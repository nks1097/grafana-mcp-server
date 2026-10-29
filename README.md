# 📊 Grafana MCP Server — 100 Ferramentas em Português

[![CI Pipeline](https://github.com/nks1097/grafana-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/nks1097/grafana-mcp-server/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![MCP Specification](https://img.shields.io/badge/MCP-2.3.0-green.svg)](https://modelcontextprotocol.io/)
[![Grafana Compatibility](https://img.shields.io/badge/Grafana-v9%20%7C%20v10%20%7C%20v11%20%7C%20v12%20%7C%20v13-orange.svg)](https://grafana.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Servidor corporativo oficial **Model Context Protocol (MCP)** para gerenciamento inteligente, observabilidade e automação do **Grafana**. Equipado com **100 ferramentas funcionais em português**, preparadas para equipes de **SRE, DevOps, NOC, SOC e Engenharia de Infraestrutura** operarem em ambientes de produção no mundo todo.

---

## 🌟 Destaques do Projeto

- 🤖 **Motor de Dashboards por Prompt (9 Estágios):** Criação autônoma de dashboards completos a partir de pedidos em linguagem natural, com validação de gridPos, layout responsivo e publicação na API.
- 🔍 **Validação Estática de Consultas:** Verificação prévia de expressões PromQL, LogQL, TraceQL e restrição estrita de leitura (`SELECT`/`WITH`) em fontes SQL relacionais contra comandos destrutivos.
- 📑 **Relatórios Executivos Multi-Formato:** Exportação nativa de relatórios de disponibilidade (SLA/SLO), desempenho e capacidade em **PDF corporativo**, planilhas **Excel (.xlsx)**, CSV e JSON.
- 🛡️ **Segurança Defensiva e RBAC:** 3 modos de operação (`somente_leitura`, `operacional`, `administrativo`), aprovação em dois passos via tokens criptográficos **HMAC-SHA256** para deleções e redação automática de credenciais.
- 🌐 **Compatibilidade Universal:** Testado e homologado no **Grafana v13.0.2**, suportando também versões 9.x, 10.x, 11.x e 12.x (OSS, Enterprise e Grafana Cloud).
- ⚡ **Transporte Duplo:** Suporte nativo tanto a **STDIO** (para IDEs locais) quanto **SSE (Server-Sent Events)** para contêineres Docker e Kubernetes em rede.

---

## 🚀 Passo a Passo de Instalação e Configuração

### 1. Pré-requisitos
- **Python 3.11 ou superior** instalado na máquina.
- Instância do **Grafana** acessível via rede (ex: `http://192.168.0.107:3000` ou `http://localhost:3000`).

---

### 2. Gerar o Token de Acesso no Grafana
O método recomendado em produção é o **Service Account Token**:
1. No menu do Grafana, navegue até **Administration** ➔ **Users and access** ➔ **Service accounts**.
2. Clique em **Add service account**, atribua o nome `mcp-server` e o papel (*Role*) `Editor` ou `Admin`.
3. Clique em **Add service account token**, copie a chave gerada (prefixo `glsa_...`).

---

### 3. Instalação Local (Ambiente Virtual)

```bash
# 1. Clone o repositório
git clone https://github.com/nks1097/grafana-mcp-server.git
cd grafana-mcp-server

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# No Linux/macOS:
source .venv/bin/activate
# No Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 3. Instale o pacote em modo editável
pip install --upgrade pip
pip install -e .
```

---

### 4. Configuração das Variáveis de Ambiente (`.env`)

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Ajuste as configurações no `.env`:
```ini
# URL da sua instância do Grafana
GRAFANA_URL=http://192.168.0.107:3000

# Token da Service Account
GRAFANA_API_TOKEN=glsa_seu_token_de_servico_aqui_exemplo12345

# Nível de Governança (somente_leitura | operacional | administrativo)
MCP_MODE=operacional
MCP_READ_ONLY=false
MCP_REQUIRE_APPROVAL_DESTRUCTIVE=true
```

---

## 💻 Integração com Clientes de IA (MCP Clients)

### A. Claude Desktop
Edite o arquivo de configuração do Claude Desktop:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "grafana-mcp": {
      "command": "C:\\SEU_CAMINHO\\grafana-mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["-m", "grafana_mcp.server", "--transport", "stdio"],
      "env": {
        "GRAFANA_URL": "http://SEU_IP:3000",
        "GRAFANA_API_TOKEN": "glsa_seu_token_de_servico_aqui_exemplo12345",
        "MCP_MODE": "operacional"
      }
    }
  }
}
```

### B. Antigravity IDE / VS Code (Continue / Cline / Roo Code)
No arquivo `mcp_config.json`:
```json
{
  "mcpServers": {
    "grafana-mcp": {
      "command": "C:\\SEU_CAMINHO\\grafana-mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["-m", "grafana_mcp.server"],
      "env": {
        "GRAFANA_URL": "http://SEU_IP:3000",
        "GRAFANA_API_TOKEN": "glsa_seu_token_de_servico_aqui_exemplo12345",
        "MCP_MODE": "operacional"
      }
    }
  }
}
```

### C. Cursor IDE
No arquivo `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "grafana-mcp": {
      "command": "python",
      "args": ["-m", "grafana_mcp.server"],
      "cwd": "C:\\SEU_CAMINHO\\grafana-mcp-server\\.venv\\Scripts\\python.exe",
      "env": {
        "GRAFANA_URL": "http://SEU_IP:3000",
        "GRAFANA_API_TOKEN": "glsa_seu_token_de_servico_aqui_exemplo12345"
      }
    }
  }
}
```
### VIDEO DE CONFIGURAÇÃO DE FORMA SIMPLIFICADA

 ▶️ **[Clique aqui para assistir ao vídeo completo no Google Drive Assiste em Full Hd (1080P)](https://drive.google.com/file/d/14ufaVIexxAb8eLNV81xWtnM-JWlvHHjP/view?usp=drive_link)**
---

## 🐳 Execução via Docker Compose (Transporte SSE)

Para executar o servidor isolado em contêiner com transporte HTTP Server-Sent Events (SSE):

```bash
docker compose up -d --build
```
O servidor estará disponível na porta `8001`: `http://localhost:8001/sse`.

---

## 📋 Catálogo Completo das 100 Ferramentas (Para que serve cada uma)

Abaixo estão listadas todas as 100 ferramentas disponíveis organizadas por categoria, com identificador oficial e finalidade prática:

### Categoria A: Dashboards e Painéis (001 a 020)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **001** | `grafana_listar_dashboards` | Pesquisa e lista dashboards cadastrados no Grafana com filtros por texto, tags e pastas. |
| **002** | `grafana_obter_dashboard` | Recupera a definição JSON completa de um dashboard pelo seu identificador único (UID). |
| **003** | `grafana_obter_resumo_dashboard` | Retorna um resumo técnico compacto (título, quantidade de painéis, variáveis) sem sobrecarregar o contexto. |
| **004** | `grafana_obter_painel` | Extrai a configuração detalhada de um único painel pelo seu ID numérico dentro de um dashboard. |
| **005** | `grafana_criar_dashboard` | Cria um novo dashboard no Grafana persistindo a estrutura JSON fornecida na pasta desejada. |
| **006** | `grafana_atualizar_dashboard` | Atualiza a definição de um dashboard existente com mensagem de commit e controle de versão. |
| **007** | `grafana_excluir_dashboard` | Exclui permanentemente um dashboard (protegido por token de aprovação em dois passos). |
| **008** | `grafana_duplicar_dashboard` | Clona um dashboard modelo com novo título, gerando novo UID e preservando painéis. |
| **009** | `grafana_gerenciar_variaveis_dashboard` | Consulta, adiciona ou atualiza variáveis dinâmicas de template (host, ambiente, interval) em dashboards. |
| **010** | `grafana_gerar_link_dashboard` | Constrói uma URL web completa e clicável com intervalo temporal e variáveis aplicadas. |
| **011** | `grafana_gerar_dashboard_por_prompt` | Motor autônomo em 9 etapas: entende o pedido, planeja painéis, valida queries e publica o dashboard. |
| **012** | `grafana_planejar_dashboard` | Gera o plano arquitetural do dashboard (estágio 3 do motor) para revisão prévia sem salvar na API. |
| **013** | `grafana_adicionar_painel` | Adiciona um novo painel com visualização configurada e posicionamento automático na grade 24 colunas. |
| **014** | `grafana_atualizar_painel` | Altera título, descrição, tipo de gráfico ou consultas de um painel específico. |
| **015** | `grafana_remover_painel` | Remove um painel específico de um dashboard pelo seu ID numérico. |
| **016** | `grafana_gerenciar_consultas_painel` | Consulta ou substitui as consultas de métricas (targets) configuradas em um painel. |
| **017** | `grafana_configurar_visualizacao` | Ajusta propriedades visuais (estilo de linha, preenchimento, modo de tooltip e legendas). |
| **018** | `grafana_configurar_limites_cores` | Configura réguas de limiares (*thresholds*) e paleta de cores (verde, amarelo, vermelho) para stat/gauges. |
| **019** | `grafana_validar_dashboard` | Valida o schema JSON do dashboard contra a especificação oficial do Grafana antes da publicação. |
| **020** | `grafana_testar_consultas_dashboard` | Pós-valida todas as consultas de todos os painéis disparando requisições de teste para certificar que retornam dados. |

### Categoria B: Fontes de Dados e Plugins (021 a 030)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **021** | `grafana_listar_fontes_dados` | Lista todas as fontes de dados configuradas (Prometheus, Loki, Tempo, Zabbix, SQL, etc.). |
| **022** | `grafana_obter_fonte_dados` | Consulta detalhes técnicos e configurações de conexão de uma datasource específica. |
| **023** | `grafana_criar_fonte_dados` | Provisiona uma nova fonte de dados no Grafana com parâmetros de rede e autenticação. |
| **024** | `grafana_atualizar_fonte_dados` | Atualiza credenciais, URL de endpoint ou opções de TLS de uma datasource existente. |
| **025** | `grafana_excluir_fonte_dados` | Remove uma fonte de dados da instância (requer token de aprovação). |
| **026** | `grafana_testar_fonte_dados` | Dispara o teste de saúde nativo do Grafana na datasource para verificar conectividade e autenticação. |
| **027** | `grafana_diagnosticar_fontes_dados` | Executa varredura de saúde em todas as fontes simultaneamente, emitindo diagnóstico geral. |
| **028** | `grafana_listar_plugins` | Lista todos os plugins instalados na instância (aplicativos, painéis e datasources). |
| **029** | `grafana_verificar_compatibilidade_plugin` | Checa se determinado plugin está presente e se é compatível com a versão instalada do Grafana. |
| **030** | `grafana_listar_fontes_por_tipo` | Retorna somente as fontes de dados de uma tecnologia específica (ex: apenas `prometheus` ou `loki`). |

### Categoria C: Consultas e Métricas (031 a 040)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **031** | `grafana_executar_consulta` | Executa consultas genéricas através do endpoint unificado `/api/ds/query` do Grafana. |
| **032** | `grafana_consultar_prometheus` | Executa consultas PromQL otimizadas diretamente em fontes Prometheus ou Mimir. |
| **033** | `grafana_consultar_loki` | Executa consultas de agregação métrica LogQL em fontes Loki. |
| **034** | `grafana_consultar_tempo` | Executa consultas TraceQL ou busca por Trace ID em fontes de rastreamento Tempo. |
| **035** | `grafana_consultar_influxdb` | Executa consultas temporais Flux ou InfluxQL em fontes InfluxDB. |
| **036** | `grafana_consultar_fonte_sql` | Executa consultas SQL estritamente de leitura (SELECT) em bancos relacionais com bloqueio preventivo de DDL/DML. |
| **037** | `grafana_executar_consulta_painel` | Executa exatamente as queries configuradas em um painel já existente, retornando os valores renderizados. |
| **038** | `grafana_comparar_metricas_periodos` | Compara uma métrica entre dois períodos temporais distintos (ex: hoje vs ontem) calculando a variação delta. |
| **039** | `grafana_analisar_tendencias_metricas` | Analisa a tendência histórica de uma métrica calculando média, desvio padrão e inclinação de crescimento. |
| **040** | `grafana_detectar_anomalias_metricas` | Identifica valores atípicos (*outliers*) aplicando cálculo de desvio padrão (Z-Score) em séries temporais. |

### Categoria D: Logs, Traces e Observabilidade (041 a 050)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **041** | `grafana_pesquisar_logs` | Pesquisa linhas de log em fontes Loki com filtros de streams e busca textual. |
| **042** | `grafana_identificar_padroes_erro` | Agrupa e quantifica padrões frequentes de mensagens de erro em logs. |
| **043** | `grafana_identificar_requisicoes_lentas` | Localiza spans de rastreamento com latência acima de um limiar pré-estabelecido. |
| **044** | `grafana_obter_detalhes_trace` | Recupera a árvore completa de spans de uma transação distribuída pelo ID do trace. |
| **045** | `grafana_comparar_traces` | Compara um trace saudável contra um trace degradado para isolar a operação gargalo. |
| **046** | `grafana_explorar_atributos_trace` | Lista tags indexadas e atributos de spans de um determinado serviço. |
| **047** | `grafana_correlacionar_logs_metricas_traces` | Realiza correlação 360° unindo métricas, logs e traces na mesma janela de tempo para um serviço. |
| **048** | `grafana_investigar_servico` | Conduz triagem diagnóstica rápida no serviço (taxa de erro, throughput e latência). |
| **049** | `grafana_diagnosticar_degradacao` | Identifica falhas em cascata no ambiente recente e aponta o provável foco inicial do incidente. |
| **050** | `grafana_gerar_linha_tempo_incidente` | Monta linha do tempo cronológica com todos os eventos, deploys e anotações durante uma parada. |

### Categoria E: Alertas e Notificações (051 a 060)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **051** | `grafana_listar_regras_alerta` | Lista todas as regras de alerta configuradas no Grafana Unified Alerting. |
| **052** | `grafana_obter_regra_alerta` | Consulta os detalhes técnicos, expressões e limiares de uma regra de alerta específica. |
| **053** | `grafana_criar_regra_alerta` | Cadastra uma nova regra de alerta com condições e labels validadas. |
| **054** | `grafana_atualizar_regra_alerta` | Modifica limiares de acionamento ou labels de uma regra existente. |
| **055** | `grafana_excluir_regra_alerta` | Remove uma regra de alerta da plataforma (requer aprovação em dois passos). |
| **056** | `grafana_listar_instancias_alerta` | Lista os alertas que estão atualmente disparados (*firing*), pendentes ou normais. |
| **057** | `grafana_gerenciar_politicas_notificacao` | Consulta ou atualiza a árvore de políticas de roteamento de notificações para as equipes. |
| **058** | `grafana_gerenciar_pontos_contato` | Lista, cadastra ou testa canais de contato como Slack, Telegram, Webhook, PagerDuty e E-mail. |
| **059** | `grafana_gerenciar_silenciamentos` | Cria, consulta ou cancela silenciamentos temporários de alertas durante manutenções programadas. |
| **060** | `grafana_diagnosticar_alertas` | Audita a saúde dos alertas, detectando regras em flapping, sem ponto de contato ou com erro de entrega. |

### Categoria F: Pastas, Tags e Anotações (061 a 070)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **061** | `grafana_listar_pastas` | Lista todas as pastas de organização de dashboards com paginação. |
| **062** | `grafana_criar_pasta` | Cria uma nova pasta no Grafana para agrupar dashboards de um projeto ou departamento. |
| **063** | `grafana_atualizar_pasta` | Renomeia uma pasta existente mantendo seus dashboards associados. |
| **064** | `grafana_excluir_pasta` | Exclui uma pasta e seus dashboards contidos (requer aprovação administrativa). |
| **065** | `grafana_mover_dashboard` | Transfere um dashboard de sua pasta atual para uma nova pasta de destino. |
| **066** | `grafana_listar_tags` | Lista todas as tags utilizadas na organização com respectiva contagem de uso. |
| **067** | `grafana_pesquisar_recursos` | Busca unificada por dashboards, pastas e painéis em um único comando por palavra-chave. |
| **068** | `grafana_gerar_link_explore` | Constrói uma URL direta para a aba Grafana Explore com a consulta pré-carregada para o operador. |
| **069** | `grafana_gerenciar_snapshots` | Cria ou lista snapshots congelados no tempo para compartilhamento público ou interno. |
| **070** | `grafana_gerenciar_anotacoes` | Registra e lista anotações na linha do tempo dos dashboards (ex: marcar momentos de deploys ou crises). |

### Categoria G: Relatórios e Renderização (071 a 080)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **071** | `grafana_gerar_relatorio_executivo` | Consolida a saúde do ambiente, datasources, dashboards e alertas em relatório PDF, Excel ou Markdown. |
| **072** | `grafana_gerar_relatorio_disponibilidade` | Emite relatório técnico de disponibilidade de serviços, percentual de SLA e tempos de indisponibilidade. |
| **073** | `grafana_gerar_relatorio_desempenho` | Gera relatório de performance com latência de API (p95/p99), QPS e consumo de recursos. |
| **074** | `grafana_gerar_relatorio_alertas` | Consolida o histórico de alarmes acionados, severidade e frequência no período. |
| **075** | `grafana_gerar_relatorio_incidentes` | Gera relatório de resposta a incidentes contendo MTTD, MTTR e resoluções aplicadas. |
| **076** | `grafana_gerar_relatorio_capacidade` | Gera relatório de planejamento de capacidade (*Capacity Planning*) com projeções para 90 dias. |
| **077** | `grafana_renderizar_painel` | Gera a URL direta do serviço Image Renderer para download de imagem PNG de um painel individual. |
| **078** | `grafana_renderizar_dashboard` | Gera a URL para captura de tela completa em alta definição de todo o dashboard em PNG. |
| **079** | `grafana_exportar_relatorio_pdf` | Exporta dados tabulares customizados fornecidos pelo agente para documento PDF corporativo formatado. |
| **080** | `grafana_exportar_relatorio_csv_excel` | Exporta matrizes de dados analíticos para planilhas Excel formatadas (`.xlsx`) ou arquivos `.csv`. |

### Categoria H: Incidentes, SLOs e OnCall (081 a 090)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **081** | `grafana_listar_incidentes` | Consulta a lista de incidentes operacionais ativos ou resolvidos no Grafana Incident. |
| **082** | `grafana_criar_incidente` | Declara formalmente um novo incidente operacional com severidade e descrição de impacto. |
| **083** | `grafana_obter_incidente` | Consulta os detalhes completos, responsáveis e status de um incidente pelo seu ID. |
| **084** | `grafana_atualizar_incidente` | Altera o status do incidente (`investigating` -> `mitigated` -> `resolved`) e adiciona resumos de ações. |
| **085** | `grafana_adicionar_atividade_incidente` | Adiciona notas, comentários ou evidências na linha do tempo de um incidente em andamento. |
| **086** | `grafana_gerenciar_agendas_oncall` | Consulta e gerencia as escalas de sobreaviso e plantão no Grafana OnCall. |
| **087** | `grafana_consultar_grupos_alerta_oncall` | Consulta grupos de alertas pendentes de atendimento na fila do plantão OnCall. |
| **088** | `grafana_consultar_slos` | Consulta os objetivos de nível de serviço (SLOs) configurados e a conformidade atual de SLIs. |
| **089** | `grafana_analisar_orcamento_erro` | Calcula o consumo do orçamento de erro (*Error Budget*) e a taxa de queima (*Burn Rate*) de um SLO. |
| **090** | `grafana_gerar_resumo_pos_incidente` | Gera minuta estruturada de relatório de pós-mortem em Markdown com RCA e plano de ação. |

### Categoria I: Administração, Governança e Auditoria (091 a 100)
| # | Ferramenta | Para que serve (Descrição) |
| :-: | :--- | :--- |
| **091** | `grafana_obter_informacoes_instancia` | Retorna a versão exata do Grafana, commit de build e integridade da base de dados. |
| **092** | `grafana_listar_organizacoes` | Lista todas as organizações cadastradas em instâncias multitenant. |
| **093** | `grafana_listar_usuarios` | Lista os usuários membros da organização atual, seus papéis (*roles*) e e-mails de acesso. |
| **094** | `grafana_listar_equipes` | Lista equipes e times de trabalho (*teams*) configurados na organização. |
| **095** | `grafana_gerenciar_equipes` | Cria, atualiza ou exclui equipes no Grafana com confirmação em dois passos para exclusão. |
| **096** | `grafana_consultar_permissoes` | Consulta a lista de controle de acesso (ACL) de um dashboard ou pasta específica. |
| **097** | `grafana_gerenciar_permissoes_dashboard` | Atribui ou modifica permissões de acesso (Viewer, Editor, Admin) de um dashboard. |
| **098** | `grafana_gerenciar_permissoes_pasta` | Define permissões herdadas por todos os dashboards contidos em determinada pasta. |
| **099** | `grafana_auditar_configuracoes` | Executa auditoria 360° de conformidade e segurança na instância, gerando pontuação (0 a 100) e alertas. |
| **100** | `grafana_testar_conexao` | Testa conectividade imediata, autenticação, mede latência em milissegundos e valida a versão do Grafana. |

---

## 🧪 Testes Automatizados

Para executar a suíte completa de testes unitários e testes de integração com a instância real do Grafana:

```bash
# Ative o ambiente virtual
.\.venv\Scripts\Activate.ps1

# Execute o pytest com relatório detalhado
pytest tests -v
```

Saída dos testes:
```text
============================= 16 passed in 2.04s ==============================
```

Para verificar estilo e conformidade de código:
```bash
ruff check src tests
ruff format --check src tests
```

---

## 📄 Documentação Adicional

Acesse a pasta [`docs/`](docs/) para guias especializados:
- [Referência Detalhada das 100 Ferramentas](docs/tools-reference.md)
- [Guia Completo de Instalação](docs/installation.md)
- [Variáveis de Ambiente e Configurações](docs/configuration.md)
- [Arquitetura e Fluxo de Dados](docs/architecture.md)
- [Motor de Criação de Dashboards (9 Estágios)](docs/dashboard-creation.md)
- [Geração de Relatórios Corporativos](docs/reports.md)
- [Segurança, RBAC e Tokens HMAC](docs/security.md)
- [Matriz de Compatibilidade do Grafana](docs/compatibility.md)
- [Guia de Solução de Problemas (Troubleshooting)](docs/troubleshooting.md)

---

## 🤝 Como Contribuir

Contribuições são muito bem-vindas! Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de desenvolvimento, padrões de commits e boas práticas de código.

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para obter detalhes completos.
