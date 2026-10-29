"""Detecção de versão e matriz de compatibilidade do Grafana."""

from typing import Any


class GrafanaCapabilities:
    """Matriz de capacidades e recursos detectados dinamicamente no Grafana."""

    def __init__(self, version_info: dict[str, Any] | None = None) -> None:
        self.raw_version = ""
        self.major = 10
        self.minor = 0
        self.has_unified_alerting = True
        self.has_service_accounts = True
        self.has_slos = False
        self.has_incidents = False
        self.has_oncall = False
        self.has_image_rendering = False

        if version_info:
            self._parse_version(version_info)

    def _parse_version(self, info: dict[str, Any]) -> None:
        version_str = str(info.get("version", ""))
        self.raw_version = version_str
        parts = version_str.split(".")
        try:
            self.major = int(parts[0]) if len(parts) > 0 else 10
            self.minor = int(parts[1]) if len(parts) > 1 else 0
        except ValueError:
            self.major = 10
            self.minor = 0

        # Zabbix / Grafana 9+ possui Service Accounts e Unified Alerting
        self.has_unified_alerting = self.major >= 9
        self.has_service_accounts = self.major >= 9

    def get_summary(self) -> dict[str, Any]:
        return {
            "versao_grafana": self.raw_version or f"{self.major}.{self.minor}",
            "versao_maior": self.major,
            "versao_menor": self.minor,
            "alertas_unificados": self.has_unified_alerting,
            "contas_servico": self.has_service_accounts,
            "slos_disponiveis": self.has_slos,
            "incidentes_disponiveis": self.has_incidents,
            "oncall_disponivel": self.has_oncall,
            "renderizacao_imagem": self.has_image_rendering,
        }
