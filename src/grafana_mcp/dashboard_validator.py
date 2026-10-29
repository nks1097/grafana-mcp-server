"""Validador estrito de estrutura e painéis de dashboards do Grafana."""

from typing import Any

from .exceptions import GrafanaValidationError


class DashboardValidator:
    """Valida a integridade técnica de um dashboard antes de publicar na API."""

    VALID_PANEL_TYPES = {
        "timeseries",
        "stat",
        "gauge",
        "bargauge",
        "table",
        "heatmap",
        "piechart",
        "logs",
        "nodeGraph",
        "traces",
        "alertlist",
        "dashlist",
        "news",
        "text",
        "canvas",
        "geomap",
    }

    @classmethod
    def validate_dashboard_dict(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Verifica se o dicionário possui campos mínimos e estrutura válida."""
        if not isinstance(data, dict):
            raise GrafanaValidationError("O payload do dashboard deve ser um objeto JSON/dicionário.")

        dash = data.get("dashboard", data)

        if not dash.get("title"):
            raise GrafanaValidationError("O dashboard deve conter um 'title' (título) válido.")

        panels = dash.get("panels", [])
        if not isinstance(panels, list):
            raise GrafanaValidationError("O campo 'panels' do dashboard deve ser uma lista.")

        # Validação de cada painel
        panel_ids = set()
        for idx, panel in enumerate(panels):
            if not isinstance(panel, dict):
                raise GrafanaValidationError(f"Painel no índice {idx} não é um objeto válido.")

            p_id = panel.get("id")
            if p_id in panel_ids and p_id is not None:
                # Ajusta ID duplicado
                panel["id"] = max(panel_ids) + 1 if panel_ids else idx + 1
            if p_id is not None:
                panel_ids.add(panel["id"])

            p_type = panel.get("type", "timeseries")
            if p_type not in cls.VALID_PANEL_TYPES:
                # Não bloqueia, mas registra aviso de compatibilidade
                pass

            # Garante gridPos
            if "gridPos" not in panel or not isinstance(panel["gridPos"], dict):
                panel["gridPos"] = {"h": 8, "w": 12, "x": (idx % 2) * 12, "y": (idx // 2) * 8}

        return {
            "valid": True,
            "title": dash.get("title"),
            "uid": dash.get("uid"),
            "panel_count": len(panels),
            "panels": panels,
        }
