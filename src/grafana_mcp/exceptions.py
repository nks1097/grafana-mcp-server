"""Hierarquia de exceções de domínio do Grafana MCP Server."""

from typing import Any


class GrafanaMCPError(Exception):
    """Exceção base do Grafana MCP Server."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        return {
            "tipo_erro": self.__class__.__name__,
            "mensagem": self.message,
            "detalhes": self.details,
        }


class GrafanaConnectionError(GrafanaMCPError):
    """Erro ao conectar com a API HTTP do Grafana."""


class GrafanaAuthError(GrafanaMCPError):
    """Erro de autenticação (Token inválido, expirado ou usuário incorreto)."""


class GrafanaPermissionError(GrafanaMCPError):
    """Erro de permissão bloqueado pelo RBAC ou pelo próprio Grafana."""


class GrafanaNotFoundError(GrafanaMCPError):
    """Recurso solicitado não foi encontrado no Grafana."""


class GrafanaValidationError(GrafanaMCPError):
    """Parâmetros de entrada inválidos ou falha na validação do dashboard/consulta."""


class GrafanaQueryError(GrafanaMCPError):
    """Erro na execução de consultas PromQL, LogQL, SQL ou Tempo."""


class GrafanaApprovalRequiredError(GrafanaMCPError):
    """Operação destrutiva requer token criptográfico de aprovação em dois passos."""


class GrafanaRateLimitError(GrafanaMCPError):
    """Limite de taxa de requisições excedido."""
