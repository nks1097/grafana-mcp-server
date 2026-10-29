"""Ponto de Entrada do Servidor MCP Grafana (FastMCP / MCPServer).

Registra as 100 ferramentas em português, recursos de observabilidade e prompts especializados.
"""

import argparse
import logging
import sys

try:
    from mcp.server.mcpserver import MCPServer
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP as MCPServer  # type: ignore

from .tools import ALL_TOOLS

# Configuração de logging seguro direcionado para stderr (para não corromper o transporte stdio)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("grafana_mcp.server")


def create_server() -> MCPServer:
    """Cria e inicializa a instância do servidor MCP com as 100 ferramentas registradas."""
    server = MCPServer(
        name="grafana-mcp",
        instructions=(
            "Servidor MCP para observabilidade inteligente no Grafana, com 100 ferramentas em português "
            "para criação automatizada de dashboards, geração e validação de consultas PromQL/LogQL, "
            "gestão de alertas, relatórios executivos (PDF/XLSX), observabilidade e administração."
        ),
        version="1.0.0",
    )

    # 1. Registro automático das 100 ferramentas
    for tool_func in ALL_TOOLS:
        server.add_tool(tool_func)

    # 2. Prompts Especializados para Agentes de IA
    @server.prompt(
        name="criar_dashboard_infraestrutura",
        description="Conduz o agente de IA pelo fluxo de 9 etapas para criar um dashboard completo no Grafana a partir de um prompt.",
    )
    def prompt_criar_dashboard(prompt_usuario: str, pasta_nome: str = "Geral") -> str:
        return (
            f"Inicie a criação de um novo dashboard no Grafana baseado no seguinte requisito:\n"
            f'"{prompt_usuario}"\n\n'
            f"Siga rigorosamente as etapas do motor de criação:\n"
            f"1. Entenda as métricas e datasources com 'grafana_listar_fontes_dados'.\n"
            f"2. Planeje a arquitetura do painel com 'grafana_planejar_dashboard'.\n"
            f"3. Valide as consultas com 'grafana_validar_consulta_promql' ou 'grafana_validar_consulta_logql'.\n"
            f"4. Gere a prévia estruturada com 'grafana_previsualizar_dashboard'.\n"
            f"5. Valide o esquema com 'grafana_validar_dashboard'.\n"
            f"6. Salve o dashboard com 'grafana_salvar_dashboard' na pasta '{pasta_nome}'.\n"
            f"7. Valide se os painéis estão recebendo dados com 'grafana_pos_validar_dashboard'.\n"
            f"8. Entregue o resultado final com a URL direta e instruções de uso."
        )

    @server.prompt(
        name="investigar_degradacao",
        description="Guia o agente de IA a investigar degradação de desempenho correlacionando métricas, logs e traces.",
    )
    def prompt_investigar_degradacao(servico: str, janela_tempo: str = "1h") -> str:
        return (
            f"Investigue o incidente / degradação no serviço '{servico}' (janela temporal: {janela_tempo}):\n"
            f"1. Consulte alertas ativos relacionados ao serviço com 'grafana_consultar_alertas_ativos'.\n"
            f"2. Analise métricas e anomalias com 'grafana_detectar_anomalias_metricas'.\n"
            f"3. Consulte logs de erro com 'grafana_executar_consulta_logs' (buscando níveis error/fatal).\n"
            f"4. Correlacione traces de alta latência com 'grafana_consultar_traces'.\n"
            f"5. Se necessário, abra ou atualize um incidente com 'grafana_criar_incidente'.\n"
            f"6. Emita diagnóstico fundamentado com hipóteses, evidências e plano de ação."
        )

    @server.prompt(
        name="gerar_relatorio_mensal",
        description="Gera relatório consolidado de disponibilidade (SLA/SLO), incidentes e capacidade operacional.",
    )
    def prompt_gerar_relatorio(periodo: str = "30d", formato: str = "pdf") -> str:
        return (
            f"Gere um relatório completo para o período {periodo} no formato {formato}:\n"
            f"1. Relatório executivo com 'grafana_gerar_relatorio_executivo'.\n"
            f"2. Relatório de disponibilidade e SLA com 'grafana_gerar_relatorio_disponibilidade'.\n"
            f"3. Consolidado de capacidade com 'grafana_gerar_relatorio_capacidade'.\n"
            f"4. Salve o documento e retorne o caminho do arquivo gerado para o operador."
        )

    @server.prompt(
        name="auditar_instancia_grafana",
        description="Executa auditoria 360° de segurança, conectividade, organização de dashboards e boas práticas.",
    )
    def prompt_auditar_grafana() -> str:
        return (
            "Execute uma auditoria completa na instância Grafana:\n"
            "1. Teste a conectividade e latência com 'grafana_testar_conexao'.\n"
            "2. Audite as configurações e segurança com 'grafana_auditar_configuracoes'.\n"
            "3. Audite as fontes de dados com 'grafana_auditar_fontes_dados'.\n"
            "4. Verifique a saúde geral com 'grafana_obter_informacoes_instancia'."
        )

    return server


def main() -> None:
    """Função principal executada ao iniciar o servidor via linha de comando."""
    parser = argparse.ArgumentParser(description="Grafana MCP Server — 100 Ferramentas em Português")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", help="Transporte MCP (stdio ou sse)")
    parser.add_argument("--host", default="127.0.0.1", help="Host para transporte SSE")
    parser.add_argument("--port", type=int, default=8001, help="Porta para transporte SSE")
    args = parser.parse_args()

    server = create_server()
    logger.info("Iniciando Grafana MCP Server (100 ferramentas carregadas)...")

    if args.transport == "sse":
        logger.info(f"Escutando em SSE http://{args.host}:{args.port}")
        server.run(transport="sse")
    else:
        logger.info("Executando em transporte STDIO...")
        server.run(transport="stdio")


if __name__ == "__main__":
    main()
