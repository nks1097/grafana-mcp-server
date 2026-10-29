"""Planejador de consultas e tradução de linguagem natural para queries técnicas."""

from typing import Any


class QueryPlanner:
    """Planeja consultas de métricas e logs a partir de solicitações em linguagem natural."""

    METRIC_TEMPLATES = {
        "cpu": {
            "prometheus": '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
            "zabbix": "system.cpu.util",
            "unit": "percent",
            "title": "Utilização de CPU (%)",
            "type": "timeseries",
        },
        "memoria": {
            "prometheus": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
            "zabbix": "vm.memory.util",
            "unit": "percent",
            "title": "Utilização de Memória (%)",
            "type": "timeseries",
        },
        "disco": {
            "prometheus": '100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)',
            "zabbix": "vfs.fs.size[/,pused]",
            "unit": "percent",
            "title": "Espaço em Disco Utilizado (%)",
            "type": "gauge",
        },
        "rede": {
            "prometheus": "rate(node_network_receive_bytes_total[5m])",
            "zabbix": "net.if.in",
            "unit": "binBps",
            "title": "Tráfego de Rede (Download)",
            "type": "timeseries",
        },
        "requisicoes": {
            "prometheus": "sum(rate(http_requests_total[5m])) by (status)",
            "zabbix": "net.tcp.service[http]",
            "unit": "reqps",
            "title": "Requisições HTTP por Segundo",
            "type": "timeseries",
        },
        "erros_http": {
            "prometheus": 'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100',
            "zabbix": "custom.http.error_rate",
            "unit": "percent",
            "title": "Taxa de Erros HTTP 5xx (%)",
            "type": "stat",
        },
        "latencia": {
            "prometheus": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "zabbix": "net.tcp.service.perf[http]",
            "unit": "s",
            "title": "Latência p95 (segundos)",
            "type": "timeseries",
        },
        "uptime": {
            "prometheus": "node_time_seconds - node_boot_time_seconds",
            "zabbix": "system.uptime",
            "unit": "s",
            "title": "Tempo de Atividade (Uptime)",
            "type": "stat",
        },
    }

    @classmethod
    def plan_query(cls, concept: str, ds_type: str = "prometheus") -> dict[str, Any]:
        """Gera a consulta recomendada, título e unidade para um determinado conceito."""
        concept_clean = concept.lower().strip()
        for key, template in cls.METRIC_TEMPLATES.items():
            if key in concept_clean:
                query = template.get(ds_type, template.get("prometheus", ""))
                return {
                    "matched": True,
                    "concept": key,
                    "title": template["title"],
                    "query": query,
                    "unit": template["unit"],
                    "panel_type": template["type"],
                }

        # Fallback genérico
        return {
            "matched": False,
            "concept": concept,
            "title": f"Métrica: {concept.title()}",
            "query": f"rate({concept.replace(' ', '_')}[5m])" if ds_type == "prometheus" else concept,
            "unit": "short",
            "panel_type": "timeseries",
        }
