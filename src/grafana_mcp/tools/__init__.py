"""Exportação consolidada de todas as 100 ferramentas do Grafana MCP Server."""

from collections.abc import Callable
from typing import Any

# Categoria I — Administração, Governança e Auditoria (091 a 100)
from .administration import (
    grafana_auditar_configuracoes,
    grafana_consultar_permissoes,
    grafana_gerenciar_equipes,
    grafana_gerenciar_permissoes_dashboard,
    grafana_gerenciar_permissoes_pasta,
    grafana_listar_equipes,
    grafana_listar_organizacoes,
    grafana_listar_usuarios,
    grafana_obter_informacoes_instancia,
    grafana_testar_conexao,
)

# Categoria E — Alertas e Notificações (051 a 060)
from .alerting import (
    grafana_atualizar_regra_alerta,
    grafana_criar_regra_alerta,
    grafana_diagnosticar_alertas,
    grafana_excluir_regra_alerta,
    grafana_gerenciar_politicas_notificacao,
    grafana_gerenciar_pontos_contato,
    grafana_gerenciar_silenciamentos,
    grafana_listar_instancias_alerta,
    grafana_listar_regras_alerta,
    grafana_obter_regra_alerta,
)

# Categoria A — Dashboards (001 a 020)
from .dashboards import (
    grafana_adicionar_painel,
    grafana_atualizar_dashboard,
    grafana_atualizar_painel,
    grafana_configurar_limites_cores,
    grafana_configurar_visualizacao,
    grafana_criar_dashboard,
    grafana_duplicar_dashboard,
    grafana_excluir_dashboard,
    grafana_gerar_dashboard_por_prompt,
    grafana_gerar_link_dashboard,
    grafana_gerenciar_consultas_painel,
    grafana_gerenciar_variaveis_dashboard,
    grafana_listar_dashboards,
    grafana_obter_dashboard,
    grafana_obter_painel,
    grafana_obter_resumo_dashboard,
    grafana_planejar_dashboard,
    grafana_remover_painel,
    grafana_testar_consultas_dashboard,
    grafana_validar_dashboard,
)

# Categoria B — Fontes de Dados (021 a 030)
from .datasources import (
    grafana_atualizar_fonte_dados,
    grafana_criar_fonte_dados,
    grafana_diagnosticar_fontes_dados,
    grafana_excluir_fonte_dados,
    grafana_listar_fontes_dados,
    grafana_listar_fontes_por_tipo,
    grafana_listar_plugins,
    grafana_obter_fonte_dados,
    grafana_testar_fonte_dados,
    grafana_verificar_compatibilidade_plugin,
)

# Categoria H — Incidentes, SLOs e OnCall (081 a 090)
from .incidents import (
    grafana_adicionar_atividade_incidente,
    grafana_analisar_orcamento_erro,
    grafana_atualizar_incidente,
    grafana_consultar_grupos_alerta_oncall,
    grafana_consultar_slos,
    grafana_criar_incidente,
    grafana_gerar_resumo_pos_incidente,
    grafana_gerenciar_agendas_oncall,
    grafana_listar_incidentes,
    grafana_obter_incidente,
)

# Categoria D — Logs, Traces e Observabilidade (041 a 050)
from .observability import (
    grafana_comparar_traces,
    grafana_correlacionar_logs_metricas_traces,
    grafana_diagnosticar_degradacao,
    grafana_explorar_atributos_trace,
    grafana_gerar_linha_tempo_incidente,
    grafana_identificar_padroes_erro,
    grafana_identificar_requisicoes_lentas,
    grafana_investigar_servico,
    grafana_obter_detalhes_trace,
    grafana_pesquisar_logs,
)

# Categoria F — Pastas, Organizações e Anotações (061 a 070)
from .organization import (
    grafana_atualizar_pasta,
    grafana_criar_pasta,
    grafana_excluir_pasta,
    grafana_gerar_link_explore,
    grafana_gerenciar_anotacoes,
    grafana_gerenciar_snapshots,
    grafana_listar_pastas,
    grafana_listar_tags,
    grafana_mover_dashboard,
    grafana_pesquisar_recursos,
)

# Categoria C — Consultas e Métricas (031 a 040)
from .queries import (
    grafana_analisar_tendencias_metricas,
    grafana_comparar_metricas_periodos,
    grafana_consultar_fonte_sql,
    grafana_consultar_influxdb,
    grafana_consultar_loki,
    grafana_consultar_prometheus,
    grafana_consultar_tempo,
    grafana_detectar_anomalias_metricas,
    grafana_executar_consulta,
    grafana_executar_consulta_painel,
)

# Categoria G — Relatórios e Renderização (071 a 080)
from .reports import (
    grafana_exportar_relatorio_csv_excel,
    grafana_exportar_relatorio_pdf,
    grafana_gerar_relatorio_alertas,
    grafana_gerar_relatorio_capacidade,
    grafana_gerar_relatorio_desempenho,
    grafana_gerar_relatorio_disponibilidade,
    grafana_gerar_relatorio_executivo,
    grafana_gerar_relatorio_incidentes,
    grafana_renderizar_dashboard,
    grafana_renderizar_painel,
)

# Lista consolidada e ordenada com todas as 100 ferramentas
ALL_TOOLS: list[Callable[..., Any]] = [
    # Categoria A (001 a 020)
    grafana_listar_dashboards,
    grafana_obter_dashboard,
    grafana_obter_resumo_dashboard,
    grafana_obter_painel,
    grafana_criar_dashboard,
    grafana_atualizar_dashboard,
    grafana_excluir_dashboard,
    grafana_duplicar_dashboard,
    grafana_gerenciar_variaveis_dashboard,
    grafana_gerar_link_dashboard,
    grafana_gerar_dashboard_por_prompt,
    grafana_planejar_dashboard,
    grafana_adicionar_painel,
    grafana_atualizar_painel,
    grafana_remover_painel,
    grafana_gerenciar_consultas_painel,
    grafana_configurar_visualizacao,
    grafana_configurar_limites_cores,
    grafana_validar_dashboard,
    grafana_testar_consultas_dashboard,
    # Categoria B (021 a 030)
    grafana_listar_fontes_dados,
    grafana_obter_fonte_dados,
    grafana_criar_fonte_dados,
    grafana_atualizar_fonte_dados,
    grafana_excluir_fonte_dados,
    grafana_testar_fonte_dados,
    grafana_diagnosticar_fontes_dados,
    grafana_listar_plugins,
    grafana_verificar_compatibilidade_plugin,
    grafana_listar_fontes_por_tipo,
    # Categoria C (031 a 040)
    grafana_executar_consulta,
    grafana_consultar_prometheus,
    grafana_consultar_loki,
    grafana_consultar_tempo,
    grafana_consultar_influxdb,
    grafana_consultar_fonte_sql,
    grafana_executar_consulta_painel,
    grafana_comparar_metricas_periodos,
    grafana_analisar_tendencias_metricas,
    grafana_detectar_anomalias_metricas,
    # Categoria D (041 a 050)
    grafana_pesquisar_logs,
    grafana_identificar_padroes_erro,
    grafana_identificar_requisicoes_lentas,
    grafana_obter_detalhes_trace,
    grafana_comparar_traces,
    grafana_explorar_atributos_trace,
    grafana_correlacionar_logs_metricas_traces,
    grafana_investigar_servico,
    grafana_diagnosticar_degradacao,
    grafana_gerar_linha_tempo_incidente,
    # Categoria E (051 a 060)
    grafana_listar_regras_alerta,
    grafana_obter_regra_alerta,
    grafana_criar_regra_alerta,
    grafana_atualizar_regra_alerta,
    grafana_excluir_regra_alerta,
    grafana_listar_instancias_alerta,
    grafana_gerenciar_politicas_notificacao,
    grafana_gerenciar_pontos_contato,
    grafana_gerenciar_silenciamentos,
    grafana_diagnosticar_alertas,
    # Categoria F (061 a 070)
    grafana_listar_pastas,
    grafana_criar_pasta,
    grafana_atualizar_pasta,
    grafana_excluir_pasta,
    grafana_mover_dashboard,
    grafana_listar_tags,
    grafana_pesquisar_recursos,
    grafana_gerar_link_explore,
    grafana_gerenciar_snapshots,
    grafana_gerenciar_anotacoes,
    # Categoria G (071 a 080)
    grafana_gerar_relatorio_executivo,
    grafana_gerar_relatorio_disponibilidade,
    grafana_gerar_relatorio_desempenho,
    grafana_gerar_relatorio_alertas,
    grafana_gerar_relatorio_incidentes,
    grafana_gerar_relatorio_capacidade,
    grafana_renderizar_painel,
    grafana_renderizar_dashboard,
    grafana_exportar_relatorio_pdf,
    grafana_exportar_relatorio_csv_excel,
    # Categoria H (081 a 090)
    grafana_listar_incidentes,
    grafana_criar_incidente,
    grafana_obter_incidente,
    grafana_atualizar_incidente,
    grafana_adicionar_atividade_incidente,
    grafana_gerenciar_agendas_oncall,
    grafana_consultar_grupos_alerta_oncall,
    grafana_consultar_slos,
    grafana_analisar_orcamento_erro,
    grafana_gerar_resumo_pos_incidente,
    # Categoria I (091 a 100)
    grafana_obter_informacoes_instancia,
    grafana_listar_organizacoes,
    grafana_listar_usuarios,
    grafana_listar_equipes,
    grafana_gerenciar_equipes,
    grafana_consultar_permissoes,
    grafana_gerenciar_permissoes_dashboard,
    grafana_gerenciar_permissoes_pasta,
    grafana_auditar_configuracoes,
    grafana_testar_conexao,
]

TOOLS_BY_NAME: dict[str, Callable[..., Any]] = {fn.__name__: fn for fn in ALL_TOOLS}
