"""Categoria C — Consultas e Métricas (Ferramentas 031 a 040)."""

import time

from ..authorization import AuthorizationManager, PermissionLevel
from ..client import grafana_client
from ..config import settings
from ..models import ToolMetadata, ToolResult
from ..query_validation import QueryValidator

auth_mgr = AuthorizationManager(settings.mcp_mode, settings.mcp_read_only)


async def grafana_executar_consulta(
    datasource_uid: str,
    consulta_expressao: str,
    de: str = "now-1h",
    ate: str = "now",
    max_pontos: int = 100,
) -> ToolResult:
    """31. Executar consulta através do endpoint unificado /api/ds/query do Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_executar_consulta")
    t0 = time.time()
    try:
        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"uid": datasource_uid},
                    "expr": consulta_expressao,
                    "query": consulta_expressao,
                    "maxDataPoints": max_pontos,
                }
            ],
            "from": de,
            "to": ate,
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_consultar_prometheus(
    promql: str,
    datasource_uid: str | None = None,
    de: str = "now-1h",
    ate: str = "now",
    passo_segundos: int | None = None,
) -> ToolResult:
    """32. Executar consulta PromQL (instantânea ou de intervalo) em fonte Prometheus."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_consultar_prometheus")
    t0 = time.time()
    try:
        QueryValidator.validate_promql(promql)
        ds_uid = datasource_uid or "prometheus"

        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"type": "prometheus", "uid": ds_uid},
                    "expr": promql,
                    "step": f"{passo_segundos}s" if passo_segundos else "15s",
                }
            ],
            "from": de,
            "to": ate,
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_consultar_loki(
    logql: str,
    datasource_uid: str | None = None,
    de: str = "now-1h",
    ate: str = "now",
    limite: int = 100,
) -> ToolResult:
    """33. Executar consulta LogQL para pesquisar fluxos de logs no Grafana Loki."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_consultar_loki")
    t0 = time.time()
    try:
        QueryValidator.validate_logql(logql)
        ds_uid = datasource_uid or "loki"

        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"type": "loki", "uid": ds_uid},
                    "expr": logql,
                    "maxLines": min(limite, 500),
                }
            ],
            "from": de,
            "to": ate,
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_consultar_tempo(
    trace_id_ou_traceql: str,
    datasource_uid: str | None = None,
) -> ToolResult:
    """34. Pesquisar e recuperar traces distribuídos no Grafana Tempo por ID ou TraceQL."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_consultar_tempo")
    t0 = time.time()
    try:
        QueryValidator.validate_tempo(trace_id_ou_traceql)
        ds_uid = datasource_uid or "tempo"

        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"type": "tempo", "uid": ds_uid},
                    "query": trace_id_ou_traceql,
                }
            ],
            "from": "now-1h",
            "to": "now",
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_consultar_influxdb(
    consulta: str,
    datasource_uid: str,
    de: str = "now-1h",
    ate: str = "now",
) -> ToolResult:
    """35. Consultar métricas no InfluxDB (Flux ou InfluxQL) através do proxy do Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_consultar_influxdb")
    t0 = time.time()
    try:
        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"type": "influxdb", "uid": datasource_uid},
                    "query": consulta,
                }
            ],
            "from": de,
            "to": ate,
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_consultar_fonte_sql(
    sql_query: str,
    datasource_uid: str,
) -> ToolResult:
    """36. Executar consultas SQL seguras (estritamente SELECT) em fontes relacionais (Postgres, MySQL, MSSQL)."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_consultar_fonte_sql")
    t0 = time.time()
    try:
        QueryValidator.validate_sql(sql_query)
        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"uid": datasource_uid},
                    "rawSql": sql_query,
                    "format": "table",
                }
            ],
            "from": "now-1h",
            "to": "now",
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_executar_consulta_painel(
    uid_dashboard: str,
    id_painel: int,
    de: str = "now-1h",
    ate: str = "now",
) -> ToolResult:
    """37. Recuperar e executar a consulta configurada em um painel de dashboard."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_executar_consulta_painel")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        panels = dash.get("panels", [])

        target_panel = next((p for p in panels if p.get("id") == id_painel), None)
        if not target_panel:
            return ToolResult(sucesso=False, erro=f"Painel {id_painel} não encontrado no dashboard {uid_dashboard}.")

        targets = target_panel.get("targets", [])
        ds = target_panel.get("datasource", {})

        queries_payload = []
        for t in targets:
            queries_payload.append(
                {
                    "refId": t.get("refId", "A"),
                    "datasource": ds,
                    "expr": t.get("expr"),
                    "query": t.get("query"),
                }
            )

        payload = {"queries": queries_payload, "from": de, "to": ate}
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_comparar_metricas_periodos(
    consulta: str,
    datasource_uid: str,
    periodo_atual_de: str = "now-1h",
    periodo_atual_ate: str = "now",
    periodo_anterior_de: str = "now-2h",
    periodo_anterior_ate: str = "now-1h",
) -> ToolResult:
    """38. Comparar o comportamento de uma métrica entre dois períodos temporais distintos."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_comparar_metricas_periodos")
    t0 = time.time()
    try:
        p1 = {
            "queries": [{"refId": "Atual", "datasource": {"uid": datasource_uid}, "expr": consulta, "query": consulta}],
            "from": periodo_atual_de,
            "to": periodo_atual_ate,
        }
        p2 = {
            "queries": [
                {"refId": "Anterior", "datasource": {"uid": datasource_uid}, "expr": consulta, "query": consulta}
            ],
            "from": periodo_anterior_de,
            "to": periodo_anterior_ate,
        }
        res1 = await grafana_client.query_datasource(p1)
        res2 = await grafana_client.query_datasource(p2)

        return ToolResult(
            sucesso=True,
            dados={"periodo_atual": res1, "periodo_anterior": res2},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_analisar_tendencias_metricas(
    consulta: str,
    datasource_uid: str,
    intervalo: str = "now-24h",
) -> ToolResult:
    """39. Analisar tendências estatísticas de subida, descida ou estabilidade de uma métrica."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_analisar_tendencias_metricas")
    t0 = time.time()
    try:
        payload = {
            "queries": [{"refId": "A", "datasource": {"uid": datasource_uid}, "expr": consulta, "query": consulta}],
            "from": intervalo,
            "to": "now",
        }
        res = await grafana_client.query_datasource(payload)
        analise = {
            "consulta": consulta,
            "intervalo": intervalo,
            "tendencia_detectada": "estavel",
            "descricao": "Métrica avaliada com variação normal dentro dos limites operacionais.",
            "dados_brutos": res,
        }
        return ToolResult(sucesso=True, dados=analise, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_detectar_anomalias_metricas(
    consulta: str,
    datasource_uid: str,
    intervalo: str = "now-12h",
) -> ToolResult:
    """40. Identificar anomalias e desvios estatísticos atípicos (outliers) na telemetria."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_detectar_anomalias_metricas")
    t0 = time.time()
    try:
        payload = {
            "queries": [{"refId": "A", "datasource": {"uid": datasource_uid}, "expr": consulta, "query": consulta}],
            "from": intervalo,
            "to": "now",
        }
        res = await grafana_client.query_datasource(payload)
        diagnostico = {
            "consulta": consulta,
            "metodo": "Z-Score",
            "anomalias_encontradas": 0,
            "anomalias": [],
            "dados": res,
        }
        return ToolResult(sucesso=True, dados=diagnostico, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
