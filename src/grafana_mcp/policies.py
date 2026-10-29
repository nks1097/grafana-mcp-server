"""Gerenciamento de políticas de confirmação em dois passos com tokens HMAC."""

import hashlib
import hmac
import json
import time
from typing import Any

from .exceptions import GrafanaApprovalRequiredError


class ApprovalPolicyManager:
    """Gera e valida tokens criptográficos HMAC para ações destrutivas."""

    def __init__(self, secret: str, ttl_seconds: int = 900) -> None:
        self.secret = secret.encode("utf-8")
        self.ttl_seconds = ttl_seconds

    def generate_token(self, action: str, params: dict[str, Any]) -> str:
        """Gera um token de aprovação assinado vinculado aos parâmetros exatos."""
        expiry = int(time.time()) + self.ttl_seconds
        payload = {
            "action": action,
            "params": params,
            "exp": expiry,
        }
        raw_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        sig = hmac.new(self.secret, raw_bytes, hashlib.sha256).hexdigest()[:32]
        return f"apr_{expiry}_{sig}"

    def validate_token(self, token: str, action: str, params: dict[str, Any]) -> bool:
        """Valida se o token HMAC confere com os parâmetros e está dentro do TTL."""
        if not token or not token.startswith("apr_"):
            return False

        parts = token.split("_")
        if len(parts) != 3:
            return False

        try:
            expiry = int(parts[1])
        except ValueError:
            return False

        if time.time() > expiry:
            return False

        payload = {
            "action": action,
            "params": params,
            "exp": expiry,
        }
        raw_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        expected_sig = hmac.new(self.secret, raw_bytes, hashlib.sha256).hexdigest()[:32]
        return hmac.compare_digest(parts[2], expected_sig)

    def verify_or_raise(self, token: str | None, action: str, params: dict[str, Any], enabled: bool = True) -> None:
        """Lança GrafanaApprovalRequiredError se a confirmação for exigida e o token for inválido."""
        if not enabled:
            return

        if not token:
            proposal_token = self.generate_token(action, params)
            raise GrafanaApprovalRequiredError(
                f"Ação destrutiva '{action}' requer aprovação explícita em dois passos. "
                f"Para confirmar a execução com estes parâmetros exatos, reenvie o comando "
                f"incluindo o parâmetro 'token_aprovacao=\"{proposal_token}\"' (válido por 15 minutos)."
            )

        if not self.validate_token(token, action, params):
            raise GrafanaApprovalRequiredError(
                f"Token de aprovação inválido, expirado ou incompatível com os parâmetros da ação '{action}'."
            )

    def generate_approval_request(self, action: str, target: Any, description: str) -> dict[str, Any]:
        """Gera requisição padronizada com token de aprovação para confirmação em dois passos."""
        token = self.generate_token(action, {"target": str(target)})
        return {
            "acao": action,
            "alvo": target,
            "descricao": description,
            "token": token,
            "instrucoes": "Para prosseguir, reenvie a chamada incluindo este token_aprovacao.",
            "validade_minutos": self.ttl_seconds // 60,
        }

    def verify_approval(self, token: str | None, action: str, target: Any) -> bool:
        """Verifica se o token de aprovação informado é válido para a ação e alvo."""
        if not token:
            return False
        return self.validate_token(token, action, {"target": str(target)})
