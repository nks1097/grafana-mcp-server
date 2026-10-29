"""Construtor inteligente de dashboards por linguagem natural em 9 estágios."""

import re
import uuid
from typing import Any

from .dashboard_validator import DashboardValidator
from .query_planner import QueryPlanner


class DashboardBuilder:
    """Orquestrador do fluxo completo de criação de dashboards a partir de prompts."""

    @classmethod
    def build_from_prompt(
        cls,
        prompt: str,
        available_datasources: list[dict[str, Any]],
        folder_id: int = 0,
        folder_uid: str | None = None,
        custom_title: str | None = None,
    ) -> dict[str, Any]:
        """
        Executa os estágios 1 a 4: Entendimento, Descoberta, Planejamento e Construção.
        Retorna o dicionário completo pronto para validação e publicação no Grafana.
        """
        # Estágio 1: Entendimento do Prompt
        prompt_lower = prompt.lower()
        title = custom_title or cls._extract_title(prompt)

        # Identificar métricas solicitadas
        detected_metrics = []
        for key in ["cpu", "memoria", "disco", "rede", "requisicoes", "erros_http", "latencia", "uptime"]:
            if key in prompt_lower:
                detected_metrics.append(key)
        if not detected_metrics:
            # Padrão básico se nada explícito for encontrado
            detected_metrics = ["cpu", "memoria", "disco", "rede"]

        # Estágio 2: Descoberta de Capacidades / Datasource
        primary_ds = cls._select_datasource(available_datasources)
        ds_type = primary_ds.get("type", "prometheus")
        ds_uid = primary_ds.get("uid", "")

        # Estágio 3: Planejamento de Layout e Painéis
        panels = []
        cur_y = 0
        panel_id = 1

        for idx, metric_name in enumerate(detected_metrics):
            plan = QueryPlanner.plan_query(metric_name, ds_type=ds_type)
            panel_type = plan["panel_type"]
            w = 12 if panel_type == "timeseries" else 6
            h = 8 if panel_type == "timeseries" else 4
            x = (idx % 2) * 12 if w == 12 else (idx % 4) * 6
            y = (idx // 2) * 8 if w == 12 else (idx // 4) * 4

            panel = {
                "id": panel_id,
                "title": plan["title"],
                "type": panel_type,
                "gridPos": {"x": x, "y": y, "w": w, "h": h},
                "datasource": {"type": ds_type, "uid": ds_uid},
                "targets": [{"refId": "A", "expr": plan["query"], "query": plan["query"], "format": "time_series"}],
                "fieldConfig": {
                    "defaults": {
                        "unit": plan["unit"],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "yellow", "value": 75},
                                {"color": "red", "value": 90},
                            ],
                        },
                    },
                    "overrides": [],
                },
            }
            panels.append(panel)
            panel_id += 1

        # Variáveis (Templating)
        variables = []
        if "ambiente" in prompt_lower or "env" in prompt_lower:
            variables.append(
                {
                    "name": "ambiente",
                    "label": "Ambiente",
                    "type": "custom",
                    "options": [
                        {"text": "Produção", "value": "prod", "selected": True},
                        {"text": "Staging", "value": "stage", "selected": False},
                        {"text": "Dev", "value": "dev", "selected": False},
                    ],
                    "current": {"text": "Produção", "value": "prod"},
                }
            )

        if "host" in prompt_lower or "servidor" in prompt_lower or "instancia" in prompt_lower:
            variables.append({"name": "host", "label": "Host", "type": "textbox", "current": {"value": ".*"}})

        # Estágio 4: Construção do Payload do Dashboard
        dash_uid = f"mcp-{uuid.uuid4().hex[:10]}"
        dashboard_payload = {
            "dashboard": {
                "id": None,
                "uid": dash_uid,
                "title": title,
                "tags": ["mcp-generated", "observability", "ai"],
                "timezone": "browser",
                "schemaVersion": 38,
                "version": 0,
                "refresh": "10s",
                "time": {"from": "now-6h", "to": "now"},
                "templating": {"list": variables},
                "panels": panels,
            },
            "folderId": folder_id,
            "folderUid": folder_uid,
            "overwrite": True,
            "message": f"Criado automaticamente pelo Grafana MCP Server via prompt: '{prompt[:60]}...'",
        }

        # Estágio 5: Pré-validação interna
        DashboardValidator.validate_dashboard_dict(dashboard_payload)

        return dashboard_payload

    @classmethod
    def _extract_title(cls, prompt: str) -> str:
        """Gera um título amigável a partir do prompt."""
        match = re.search(r"dashboard\s+(?:de\s+|para\s+)?([a-zA-Z0-9_\-\s]{3,30})", prompt, re.IGNORECASE)
        if match:
            return f"Dashboard {match.group(1).strip().title()}"
        return f"Dashboard Observabilidade {uuid.uuid4().hex[:6]}"

    @classmethod
    def _select_datasource(cls, datasources: list[dict[str, Any]]) -> dict[str, Any]:
        """Seleciona a melhor fonte de dados disponível."""
        if not datasources:
            return {"type": "prometheus", "uid": "prometheus", "name": "Prometheus Default"}

        # Priorizar default
        for ds in datasources:
            if ds.get("isDefault"):
                return ds

        # Priorizar prometheus ou zabbix
        for ds in datasources:
            if ds.get("type") in ("prometheus", "alexanderzobnin-zabbix-datasource"):
                return ds

        return datasources[0]
