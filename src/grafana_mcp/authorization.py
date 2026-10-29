"""Controle de acesso baseado em funções (RBAC) do Grafana MCP Server."""

from enum import StrEnum

from .exceptions import GrafanaPermissionError


class PermissionLevel(StrEnum):

    READ_ONLY = "somente_leitura"
    OPERATIONAL = "operacional"
    ADMINISTRATIVE = "administrativo"


class AuthorizationManager:
    """Valida se uma operação pode ser executada conforme o modo do servidor."""

    def __init__(self, current_mode: str, read_only_override: bool = False) -> None:
        if read_only_override:
            self.mode = PermissionLevel.READ_ONLY
        else:
            try:
                self.mode = PermissionLevel(current_mode.lower())
            except ValueError:
                self.mode = PermissionLevel.READ_ONLY

    def check_permission(self, required_level: PermissionLevel, action_name: str) -> None:
        """Verifica se o modo atual satisfaz o nível de permissão exigido."""
        hierarchy = {
            PermissionLevel.READ_ONLY: 1,
            PermissionLevel.OPERATIONAL: 2,
            PermissionLevel.ADMINISTRATIVE: 3,
        }

        current_val = hierarchy.get(self.mode, 1)
        required_val = hierarchy.get(required_level, 1)

        if current_val < required_val:
            raise GrafanaPermissionError(
                f"Operação '{action_name}' bloqueada: requer nível '{required_level.value}', "
                f"mas o servidor está operando no modo restrito '{self.mode.value}'."
            )
