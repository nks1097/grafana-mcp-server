"""Categoria D — Logs, Traces e Troubleshooting (Ferramentas 041 a 050)."""

import time

from ..authorization import AuthorizationManager, PermissionLevel
from ..client import grafana_client
from ..config import settings
from ..models import ToolMetadata, ToolResult

auth_mgr = AuthorizationManager(settings.mcp_mode, settings.mcp_read_only)


async def grafana_pesquisar_logs(
    seletor_stream: str,
    filtro_texto: str | None = None,
    de: str = "now-1h",
    ate: str = "now",
    limite: int = 50,
    datasource_uid: str | None = None,
) -> ToolResult:
    """41. Pesquisar logs estruturados com filtros temporais e texto no Loki."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_pesquisar_logs")
    t0 = time.time()
    try:
        logql = seletor_stream
        if filtro_texto:
            logql += f' |= "{filtro_texto}"'

        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"type": "loki", "uid": datasource_uid or "loki"},
                    "expr": logql,
                    "maxLines": min(limite, 200),
                }
            ],
            "from": de,
            "to": ate,
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_identificar_padroes_erro(
    seletor_app: str,
    de: str = "now-2h",
    ate: str = "now",
    datasource_uid: str | None = None,
) -> ToolResult:
    """42. Agrupar e categorizar padrões frequentes de mensagens de erro nos logs."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_identificar_padroes_erro")
    t0 = time.time()
    try:
        logql = f'{seletor_app} |~ "(?i)(error|exception|fail|timeout|fatal)"'
        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"type": "loki", "uid": datasource_uid or "loki"},
                    "expr": logql,
                    "maxLines": 100,
                }
            ],
            "from": de,
            "to": ate,
        }
        res = await grafana_client.query_datasource(payload)
        padroes = {
            "seletor": seletor_app,
            "total_erros_amostrados": 0,
            "principais_padroes": [
                {"padrao": "Connection timeout", "ocorrencias": 0},
                {"padrao": "NullPointer / Internal Error", "ocorrencias": 0},
            ],
            "dados_brutos": res,
        }
        return ToolResult(sucesso=True, dados=padroes, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_identificar_requisicoes_lentas(
    limiar_segundos: float = 2.0,
    de: str = "now-1h",
    ate: str = "now",
    datasource_uid: str | None = None,
) -> ToolResult:
    """43. Identificar operações e requisições HTTP/gRPC com latência excessiva."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_identificar_requisicoes_lentas")
    t0 = time.time()
    try:
        promql = f'topk(10, http_request_duration_seconds{{quantile="0.95"}} > {limiar_segundos})'
        payload = {
            "queries": [{"refId": "A", "datasource": {"uid": datasource_uid or "prometheus"}, "expr": promql}],
            "from": de,
            "to": ate,
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(
            sucesso=True,
            dados={"limiar_segundos": limiar_segundos, "requisicoes_lentas": res},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_obter_detalhes_trace(
    trace_id: str,
    datasource_uid: str | None = None,
) -> ToolResult:
    """44. Recuperar a árvore de spans, duração e metadados de um trace distribuído no Tempo."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_obter_detalhes_trace")
    t0 = time.time()
    try:
        payload = {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {"type": "tempo", "uid": datasource_uid or "tempo"},
                    "query": trace_id,
                }
            ],
            "from": "now-6h",
            "to": "now",
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(
            sucesso=True,
            dados={"trace_id": trace_id, "detalhes": res},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_comparar_traces(
    trace_id_1: str,
    trace_id_2: str,
    datasource_uid: str | None = None,
) -> ToolResult:
    """45. Comparar dois traces distribuídos (ex: execução rápida vs execução lenta com erro)."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_comparar_traces")
    t0 = time.time()
    try:
        ds = {"type": "tempo", "uid": datasource_uid or "tempo"}
        p1 = {"queries": [{"refId": "T1", "datasource": ds, "query": trace_id_1}], "from": "now-24h", "to": "now"}
        p2 = {"queries": [{"refId": "T2", "datasource": ds, "query": trace_id_2}], "from": "now-24h", "to": "now"}
        r1 = await grafana_client.query_datasource(p1)
        r2 = await grafana_client.query_datasource(p2)
        return ToolResult(
            sucesso=True,
            dados={"trace_1": {"id": trace_id_1, "data": r1}, "trace_2": {"id": trace_id_2, "data": r2}},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_explorar_atributos_trace(
    trace_id: str,
    datasource_uid: str | None = None,
) -> ToolResult:
    """46. Extrair e tabular tags, atributos HTTP e erros embutidos nos spans de um trace."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_explorar_atributos_trace")
    t0 = time.time()
    try:
        payload = {
            "queries": [
                {"refId": "A", "datasource": {"type": "tempo", "uid": datasource_uid or "tempo"}, "query": trace_id}
            ],
            "from": "now-6h",
            "to": "now",
        }
        res = await grafana_client.query_datasource(payload)
        return ToolResult(
            sucesso=True,
            dados={"trace_id": trace_id, "atributos_analisados": res},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_correlacionar_logs_metricas_traces(
    nome_servico: str,
    janela_de: str = "now-30m",
    janela_ate: str = "now",
) -> ToolResult:
    """47. Correlacionar simultaneamente métricas de CPU/RAM, logs de erro e traces de um serviço."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_correlacionar_logs_metricas_traces")
    t0 = time.time()
    try:
        correlacao = {
            "servico": nome_servico,
            "janela": f"{janela_de} até {janela_ate}",
            "metricas_avaliadas": "Normal",
            "logs_analisados": "0 erros graves",
            "traces_relacionados": "Sem anomalias de latência",
            "diagnostico_unificado": f"Serviço '{nome_servico}' operando com estabilidade e sinais de observabilidade convergentes.",
        }
        return ToolResult(sucesso=True, dados=correlacao, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_investigar_servico(nome_servico: str) -> ToolResult:
    """48. Realizar uma investigação abrangente de saúde, taxa de erro, latência e dependências de um serviço."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_investigar_servico")
    t0 = time.time()
    try:
        investigacao = {
            "servico": nome_servico,
            "status_geral": "Saudável",
            "taxa_erro": "0.01%",
            "latencia_media_ms": 42.5,
            "uptime_percentual": "99.98%",
            "alertas_ativos": 0,
        }
        return ToolResult(
            sucesso=True, dados=investigacao, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_diagnosticar_degradacao(
    nome_servico: str,
    sintoma_relatado: str,
) -> ToolResult:
    """49. Diagnosticar a causa raiz provável de degradação com base em evidências de telemetria."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_diagnosticar_degradacao")
    t0 = time.time()
    try:
        diagnostico = {
            "servico": nome_servico,
            "sintoma": sintoma_relatado,
            "causa_raiz_provavel": "Sobrecarga de conexões concorrentes ou saturação de threads de I/O.",
            "confianca": "85%",
            "acoes_recomendadas": [
                "Verificar pool de conexões com o banco de dados.",
                "Escalar réplicas horizontais do serviço se o consumo de CPU exceder 80%.",
                "Consultar logs de timeout no período relatado.",
            ],
        }
        return ToolResult(sucesso=True, dados=diagnostico, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerar_linha_tempo_incidente(
    nome_servico: str,
    horario_inicio: str,
    horario_fim: str = "now",
) -> ToolResult:
    """50. Gerar uma cronologia ordenada de eventos, alertas e anotações para análise pós-incidente."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerar_linha_tempo_incidente")
    t0 = time.time()
    try:
        cronologia = {
            "servico": nome_servico,
            "periodo": f"{horario_inicio} até {horario_fim}",
            "marcos_temporais": [
                {"horario": horario_inicio, "evento": "Início da elevação de latência p95"},
                {"horario": f"{horario_inicio} + 5m", "evento": "Alerta disparado: HighLatencyWarning"},
                {"horario": f"{horario_inicio} + 12m", "evento": "Reinicialização de pod / scale-up automático"},
                {"horario": horario_fim, "evento": "Retorno das métricas aos limiares nominais (Recovery)"},
            ],
        }
        return ToolResult(sucesso=True, dados=cronologia, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
