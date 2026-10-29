"""Mecanismos de autenticação para a API do Grafana."""

import base64


class GrafanaAuth:
    """Gerenciador de cabeçalhos de autenticação para o Grafana."""

    def __init__(
        self,
        token: str | None = None,
        user: str | None = None,
        password: str | None = None,
        org_id: int = 1,
    ) -> None:
        self.token = token
        self.user = user
        self.password = password
        self.org_id = org_id

    def get_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Grafana-Org-Id": str(self.org_id),
        }

        if self.token:
            clean_token = self.token.strip()
            # Suporta Service Account tokens (glsa_...) e API keys tradicionais
            headers["Authorization"] = f"Bearer {clean_token}"
        elif self.user and self.password:
            # Fallback para Basic Auth
            creds = f"{self.user}:{self.password}"
            b64 = base64.b64encode(creds.encode()).decode()
            headers["Authorization"] = f"Basic {b64}"

        return headers

    def redact_secret(self, text: str) -> str:
        """Mascara o token ou senha em strings e logs."""
        redacted = text
        if self.token and len(self.token) > 8:
            redacted = redacted.replace(self.token, f"{self.token[:4]}...[REDACTED]")
        if self.password and len(self.password) > 3:
            redacted = redacted.replace(self.password, "[REDACTED]")
        return redacted
