# 📚 Referência Completa das 100 Ferramentas MCP do Grafana

Este documento contém o catálogo exaustivo das **100 ferramentas em português** disponibilizadas pelo **Grafana MCP Server**, organizadas por categorias funcionais, detalhando **para que serve**, **quando usar**, parâmetros de entrada e retornos esperados.

---

## Índice por Categoria

- [Categoria A: Dashboards e Painéis (001 a 020)](#categoria-a-dashboards-e-painéis-001-a-020)
- [Categoria B: Fontes de Dados e Plugins (021 a 030)](#categoria-b-fontes-de-dados-e-plugins-021-a-030)
- [Categoria C: Consultas e Métricas (031 a 040)](#categoria-c-consultas-e-métricas-031-a-040)
- [Categoria D: Logs, Traces e Observabilidade (041 a 050)](#categoria-d-logs-traces-e-observabilidade-041-a-050)
- [Categoria E: Alertas e Notificações (051 a 060)](#categoria-e-alertas-e-notificações-051-a-060)
- [Categoria F: Pastas, Tags e Anotações (061 a 070)](#categoria-f-pastas-tags-e-anotações-061-a-070)
- [Categoria G: Relatórios e Renderização (071 a 080)](#categoria-g-relatórios-e-renderização-071-a-080)
- [Categoria H: Incidentes, SLOs e OnCall (081 a 090)](#categoria-h-incidentes-slos-e-oncall-081-a-090)
- [Categoria I: Administração, Governança e Auditoria (091 a 100)](#categoria-i-administração-governança-e-auditoria-091-a-100)

---

## Categoria A: Dashboards e Painéis (001 a 020)

### 001. `grafana_listar_dashboards`
- **Para que serve:** Lista todos os dashboards cadastrados no Grafana com suporte a filtros por termo de busca, tags e ID de pasta.
- **Quando usar:** Sempre que o operador ou agente precisar descobrir quais dashboards existem na instância ou localizar painéis específicos.
- **Parâmetros:**
  - `consulta` (*str | None*): Palavra-chave para busca de títulos.
  - `tag` (*str | None*): Filtrar por tag específica (ex: `producao`, `kubernetes`).
  - `pasta_ids` (*list[int] | None*): Lista de IDs numéricos de pastas.
  - `limite` (*int*, padrão `100`): Quantidade máxima de registros retornados.
  - `pagina` (*int*, padrão `1`): Número da página para paginação.
- **Retorno:** Lista de objetos contendo `uid`, `title`, `url`, `folderTitle` e `tags`.

### 002. `grafana_obter_dashboard`
- **Para que serve:** Recupera o JSON completo com toda a estrutura técnica, painéis, variáveis e configurações do dashboard.
- **Quando usar:** Antes de editar, clonar ou auditar os painéis de um dashboard existente.
- **Parâmetros:**
  - `uid` (*str*): Identificador único (UID) do dashboard.
- **Retorno:** Objeto com a chave `dashboard` contendo o modelo Grafana completo.

### 003. `grafana_obter_resumo_dashboard`
- **Para que serve:** Fornece um resumo técnico compacto (título, quantidade de painéis, variáveis e datasources utilizadas) sem carregar o JSON massivo.
- **Quando usar:** Quando o agente de IA precisar entender rapidamente a finalidade de um dashboard sem consumir excesso de contexto.
- **Parâmetros:**
  - `uid` (*str*): Identificador único do dashboard.
- **Retorno:** Objeto sintetizado com estatísticas e metadados estruturados.

### 004. `grafana_obter_painel`
- **Para que serve:** Extrai a definição isolada de um único painel dentro de um dashboard pelo seu ID numérico.
- **Quando usar:** Para inspecionar as queries, tipo de visualização ou limites de um painel específico.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard que contém o painel.
  - `id_painel` (*int*): ID numérico do painel.
- **Retorno:** Dicionário com a configuração do painel (`targets`, `fieldConfig`, `gridPos`, etc.).

### 005. `grafana_criar_dashboard`
- **Para que serve:** Cria um novo dashboard no Grafana publicando a definição JSON fornecida.
- **Quando usar:** Para publicar painéis novos na pasta raiz ou em pastas departamentais.
- **Parâmetros:**
  - `dashboard_dict` (*dict*): Estrutura JSON completa do dashboard.
  - `pasta_uid` (*str | None*): UID da pasta onde será salvo.
  - `mensagem_commit` (*str*, padrão `"Criado via MCP Server"`): Descrição da versão no histórico.
  - `sobrescrever` (*bool*, padrão `False`): Se deve substituir caso já exista.
- **Retorno:** UID, URL pública e número da versão gerada.

### 006. `grafana_atualizar_dashboard`
- **Para que serve:** Atualiza a definição de um dashboard existente mantendo o histórico de versões.
- **Quando usar:** Ao adicionar painéis, alterar queries ou atualizar variáveis.
- **Parâmetros:**
  - `dashboard_dict` (*dict*): Estrutura JSON atualizada do dashboard contendo o campo `uid`.
  - `mensagem_commit` (*str*): Motivo da alteração gravado no log de versões.
  - `pasta_uid` (*str | None*): UID da pasta de destino.
- **Retorno:** Status da atualização, nova versão e URL.

### 007. `grafana_excluir_dashboard`
- **Para que serve:** Remove permanentemente um dashboard da instância do Grafana.
- **Quando usar:** Limpeza de dashboards obsoletos (requer aprovação se o modo estrito estiver ativo).
- **Parâmetros:**
  - `uid` (*str*): UID do dashboard a ser excluído.
  - `token_aprovacao` (*str | None*): Token criptográfico HMAC de aprovação em dois passos.
- **Retorno:** Confirmação de exclusão ou requisição de token de aprovação.

### 008. `grafana_duplicar_dashboard`
- **Para que serve:** Clona um dashboard existente com novo título, gerando novo UID e preservando painéis e variáveis.
- **Quando usar:** Criação de dashboards de homologação ou réplicas para novos clientes/serviços.
- **Parâmetros:**
  - `uid_origem` (*str*): UID do dashboard modelo.
  - `novo_titulo` (*str*): Título para o novo dashboard clonado.
  - `pasta_destino_uid` (*str | None*): Pasta onde o clone será salvo.
- **Retorno:** UID e URL do novo dashboard criado.

### 009. `grafana_gerenciar_variaveis_dashboard`
- **Para que serve:** Consulta, adiciona ou atualiza variáveis de template (`query`, `custom`, `interval`) em dashboards.
- **Quando usar:** Para habilitar filtros dinâmicos de host, ambiente ou serviço nos painéis.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `acao` (*str*): `"consultar"`, `"adicionar"` ou `"atualizar"`.
  - `variavel_dados` (*dict | None*): Objeto com `name`, `type`, `query`, `datasource`.
- **Retorno:** Lista de variáveis ativas ou confirmação de inclusão.

### 010. `grafana_gerar_link_dashboard`
- **Para que serve:** Constrói uma URL web completa e funcional para visualização do dashboard com intervalo de tempo e variáveis aplicadas.
- **Quando usar:** Para fornecer um link direto e clicável ao operador de suporte ou usuário final.
- **Parâmetros:**
  - `uid` (*str*): UID do dashboard.
  - `de` (*str*, padrão `"now-6h"`): Início do período (ex: `now-24h`).
  - `ate` (*str*, padrão `"now"`): Fim do período.
  - `variaveis` (*dict | None*): Dicionário de filtros de variáveis (ex: `{"var-env": "prod"}`).
- **Retorno:** Objeto com a URL completa formatada.

### 011. `grafana_gerar_dashboard_por_prompt`
- **Para que serve:** Executa o fluxo autônomo completo em 9 estágios: entende a intenção, descobre métricas, planeja visualizações, valida queries, monta o gridPos e publica o dashboard.
- **Quando usar:** Criação ágil de dashboards completos a partir de pedidos em linguagem natural (ex: "Crie um dashboard de monitoramento de servidores Linux com CPU, memória e disco").
- **Parâmetros:**
  - `prompt` (*str*): Solicitação do usuário em linguagem natural.
  - `pasta_nome` (*str*, padrão `"Geral"`): Pasta onde será publicado.
  - `publicar_direto` (*bool*, padrão `True`): Se já deve salvar na API do Grafana.
- **Retorno:** Detalhes dos 9 estágios, UID do dashboard criado e URL de acesso.

### 012. `grafana_planejar_dashboard`
- **Para que serve:** Gera o plano arquitetural do dashboard (estágio 3 do motor de criação), selecionando painéis, tipos de gráficos e queries sem publicar na API.
- **Quando usar:** Para apresentar uma proposta técnica ao operador e solicitar validação prévia.
- **Parâmetros:**
  - `prompt` (*str*): Descrição dos requisitos do dashboard.
- **Retorno:** Plano estruturado com layout de grid, painéis e consultas sugeridas.

### 013. `grafana_adicionar_painel`
- **Para que serve:** Adiciona um novo painel com visualização configurada e posicionamento automático na grade.
- **Quando usar:** Expansão de dashboards existentes com novas métricas.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard de destino.
  - `titulo` (*str*): Título do painel.
  - `tipo_visualizacao` (*str*, padrão `"timeseries"`): Tipo (`timeseries`, `stat`, `gauge`, `table`, etc.).
  - `consultas` (*list[dict]*): Lista de consultas (`targets`).
  - `largura` (*int*, padrão `12`): Largura no grid (máx 24).
  - `altura` (*int*, padrão `8`): Altura no grid.
- **Retorno:** ID numérico do painel adicionado e nova versão do dashboard.

### 014. `grafana_atualizar_painel`
- **Para que serve:** Modifica título, descrição, tipo de gráfico ou queries de um painel existente.
- **Quando usar:** Ajustes de layout ou correção de fórmulas em painéis específicos.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `id_painel` (*int*): ID do painel a modificar.
  - `alteracoes` (*dict*): Campos a atualizar.
- **Retorno:** Confirmação da alteração e versão atualizada.

### 015. `grafana_remover_painel`
- **Para que serve:** Remove um painel específico de um dashboard pelo seu ID numérico.
- **Quando usar:** Exclusão de gráficos obsoletos ou duplicados.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `id_painel` (*int*): ID do painel a ser excluído.
- **Retorno:** Confirmação de remoção e quantidade restante de painéis.

### 016. `grafana_gerenciar_consultas_painel`
- **Para que serve:** Consulta, adiciona ou atualiza targets de consulta individuais dentro de um painel.
- **Quando usar:** Para manipular queries de métricas (PromQL, LogQL, SQL) em painéis complexos.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `id_painel` (*int*): ID do painel.
  - `acao` (*str*): `"consultar"` ou `"substituir"`.
  - `novos_targets` (*list[dict] | None*): Lista de novas consultas.
- **Retorno:** Consultas associadas ao painel.

### 017. `grafana_configurar_visualizacao`
- **Para que serve:** Configura opções visuais finas (estilo de linha, preenchimento, modo de tooltip, legenda e empilhamento).
- **Quando usar:** Padronização estética e legibilidade de gráficos corporativos.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `id_painel` (*int*): ID do painel.
  - `opcoes_custom` (*dict*): Configurações (`drawStyle`, `fillOpacity`, `gradientMode`, etc.).
- **Retorno:** Confirmação da aplicação visual.

### 018. `grafana_configurar_limites_cores`
- **Para que serve:** Define regras de limiares (*thresholds*) e paleta de cores (ex: verde até 70%, amarelo até 85%, vermelho acima de 85%).
- **Quando usar:** Painéis de alerta, indicadores de stat, gauges e cartões de SLA.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `id_painel` (*int*): ID do painel.
  - `passos_limite` (*list[dict]*): Lista de limiares com `value` e `color`.
  - `modo` (*str*, padrão `"absolute"`): `"absolute"` ou `"percentage"`.
- **Retorno:** Confirmação da configuração de cores e limites.

### 019. `grafana_validar_dashboard`
- **Para que serve:** Executa validação estática rigorosa do schema do dashboard (verificando `gridPos`, tipos de painéis suportados, UIDs e integridade).
- **Quando usar:** Antes de publicar ou salvar qualquer dashboard na API.
- **Parâmetros:**
  - `dashboard_dict` (*dict*): Estrutura JSON a ser validada.
- **Retorno:** Objeto com `valido: bool`, lista de erros e advertências.

### 020. `grafana_testar_consultas_dashboard`
- **Para que serve:** Pós-valida todas as consultas de todos os painéis do dashboard disparando requisições de teste à API de dados para verificar se retornam séries válidas ou erros.
- **Quando usar:** Imediatamente após a publicação para garantir que nenhum painel exiba mensagem de erro para o usuário final.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard recém-salvo.
- **Retorno:** Relatório detalhado com status de execução de cada painel.

---

## Categoria B: Fontes de Dados e Plugins (021 a 030)

### 021. `grafana_listar_fontes_dados`
- **Para que serve:** Lista todas as fontes de dados (*datasources*) configuradas no Grafana, incluindo Prometheus, Loki, Tempo, Zabbix, PostgreSQL, etc.
- **Quando usar:** Para descobrir quais fontes estão disponíveis e obter seus UIDs para criação de painéis.
- **Parâmetros:** Nenhum.
- **Retorno:** Lista de fontes contendo `uid`, `name`, `type`, `isDefault`, `url`.

### 022. `grafana_obter_fonte_dados`
- **Para que serve:** Consulta detalhes de conexão, configurações JSON e versão de uma datasource específica pelo UID ou ID.
- **Quando usar:** Para inspecionar propriedades de rede e autenticação de uma fonte.
- **Parâmetros:**
  - `uid_ou_id` (*str*): UID ou ID numérico da fonte de dados.
- **Retorno:** Objeto completo da fonte de dados (com senhas e segredos devidamente mascarados).

### 023. `grafana_criar_fonte_dados`
- **Para que serve:** Registra uma nova fonte de dados no Grafana.
- **Quando usar:** Onboarding automatizado de novas ferramentas de coleta.
- **Parâmetros:**
  - `fonte_payload` (*dict*): Estrutura contendo `name`, `type`, `url`, `access`, etc.
- **Retorno:** UID e ID da fonte de dados criada.

### 024. `grafana_atualizar_fonte_dados`
- **Para que serve:** Altera configurações, URL de endpoint ou credenciais de uma datasource existente.
- **Quando usar:** Migração de endpoints ou rotação de credenciais.
- **Parâmetros:**
  - `uid` (*str*): UID da fonte a atualizar.
  - `fonte_payload` (*dict*): Dados modificados.
- **Retorno:** Objeto da fonte atualizada.

### 025. `grafana_excluir_fonte_dados`
- **Para que serve:** Remove uma fonte de dados do Grafana.
- **Quando usar:** Descomissionamento de fontes antigas (requer aprovação administrativa).
- **Parâmetros:**
  - `uid` (*str*): UID da fonte.
  - `token_aprovacao` (*str | None*): Token criptográfico HMAC.
- **Retorno:** Confirmação de exclusão.

### 026. `grafana_testar_fonte_dados`
- **Para que serve:** Executa o teste de saúde e conectividade nativo do Grafana na fonte de dados especificada.
- **Quando usar:** Para confirmar se o Grafana consegue alcançar e autenticar na fonte de dados remota.
- **Parâmetros:**
  - `uid` (*str*): UID da fonte a testar.
- **Retorno:** Status da conexão (`success`, `error`), mensagem explicativa e tempo de resposta.

### 027. `grafana_diagnosticar_fontes_dados`
- **Para que serve:** Executa uma varredura de saúde em **todas** as fontes cadastradas simultaneamente.
- **Quando usar:** Rotinas de healthcheck, troubleshooting geral e auditorias preventivas.
- **Parâmetros:** Nenhum.
- **Retorno:** Matriz com o status de cada fonte, percentual de fontes saudáveis e alertas.

### 028. `grafana_listar_plugins`
- **Para que serve:** Lista todos os plugins instalados (aplicativos, painéis e datasources) e sua versão.
- **Quando usar:** Para verificar se plugins como Zabbix, Image Renderer, Incident ou SLO estão presentes.
- **Parâmetros:**
  - `tipo` (*str | None*): Filtrar por tipo (`datasource`, `panel`, `app`).
- **Retorno:** Lista de plugins com `id`, `name`, `type`, `version`.

### 029. `grafana_verificar_compatibilidade_plugin`
- **Para que serve:** Checa se determinado plugin está instalado e é compatível com a versão do Grafana.
- **Quando usar:** Antes de criar painéis especializados que dependem de plugins opcionais.
- **Parâmetros:**
  - `plugin_id` (*str*): Identificador do plugin (ex: `alexanderzobnin-zabbix-datasource`).
- **Retorno:** Objeto com `instalado: bool`, `versao` e compatibilidade.

### 030. `grafana_listar_fontes_por_tipo`
- **Para que serve:** Retorna apenas as fontes de dados correspondentes a um tipo específico.
- **Quando usar:** Quando o agente de IA precisa encontrar uma fonte Prometheus, Loki ou Zabbix disponível.
- **Parâmetros:**
  - `tipo` (*str*): Tipo da fonte (ex: `prometheus`, `loki`, `tempo`, `mysql`, `zabbix`).
- **Retorno:** Lista filtrada de fontes de dados.

---

## Categoria C: Consultas e Métricas (031 a 040)

### 031. `grafana_executar_consulta`
- **Para que serve:** Executa consultas genéricas através do endpoint unificado `/api/ds/query` do Grafana.
- **Quando usar:** Para disparar queries diretas e obter valores instantâneos ou intervalos de métricas.
- **Parâmetros:**
  - `datasource_uid` (*str*): UID da fonte de dados a consultar.
  - `queries` (*list[dict]*): Definição dos targets de consulta.
  - `de` (*str*, padrão `"now-1h"`): Início do período.
  - `ate` (*str*, padrão `"now"`): Fim do período.
- **Retorno:** Séries temporais, frames de dados e metadados retornados pela fonte.

### 032. `grafana_consultar_prometheus`
- **Para que serve:** Executa consultas PromQL otimizadas diretamente em datasources Prometheus ou Mimir.
- **Quando usar:** Análise de métricas de infraestrutura, Kubernetes, CPU, memória e requisições HTTP.
- **Parâmetros:**
  - `promql` (*str*): Expressão PromQL (ex: `rate(node_cpu_seconds_total[5m])`).
  - `datasource_uid` (*str | None*): UID da fonte (se omitido, usa a fonte Prometheus padrão).
  - `de` (*str*, padrão `"now-1h"`): Início do intervalo.
  - `ate` (*str*, padrão `"now"`): Fim do intervalo.
  - `passo` (*str*, padrão `"15s"`): Intervalo de resolução temporal (*step*).
- **Retorno:** Séries temporais com rótulos e pares `[timestamp, valor]`.

### 033. `grafana_consultar_loki`
- **Para que serve:** Executa consultas de métricas e agregações LogQL em datasources Loki.
- **Quando usar:** Contagem de taxas de logs, volumes de mensagens por segundo e análise de tendências de logs.
- **Parâmetros:**
  - `logql` (*str*): Expressão LogQL (ex: `rate({app="nginx"} |= "error" [5m])`).
  - `datasource_uid` (*str | None*): UID da fonte Loki.
  - `de` (*str*, padrão `"now-1h"`): Período inicial.
  - `ate` (*str*, padrão `"now"`): Período final.
- **Retorno:** Matriz de métricas agregadas por rótulo.

### 034. `grafana_consultar_tempo`
- **Para que serve:** Executa consultas de rastreamento distribuído (TraceQL ou busca por Trace ID) no Tempo.
- **Quando usar:** Diagnóstico de latência em microsserviços e rastreamento de requisições lentas.
- **Parâmetros:**
  - `query` (*str*): Expressão TraceQL ou ID de trace.
  - `datasource_uid` (*str | None*): UID da fonte Tempo.
- **Retorno:** Spans de trace com tempos de início, duração, tags e eventos de erro.

### 035. `grafana_consultar_influxdb`
- **Para que serve:** Executa consultas em bancos de séries temporais InfluxDB (Flux ou InfluxQL).
- **Quando usar:** Consulta de sensores IoT, telemetria de rede e dados temporais legado.
- **Parâmetros:**
  - `query` (*str*): Expressão Flux ou InfluxQL.
  - `datasource_uid` (*str*): UID da fonte InfluxDB.
- **Retorno:** Tabelas ou séries de métricas.

### 036. `grafana_consultar_fonte_sql`
- **Para que serve:** Executa consultas analíticas estritamente de leitura (SELECT/WITH) em fontes relacionais (PostgreSQL, MySQL, SQLite, ClickHouse) com bloqueio preventivo de comandos destrutivos.
- **Quando usar:** Consulta de cadastros, tabelas de inventário e métricas armazenadas em bancos SQL.
- **Parâmetros:**
  - `datasource_uid` (*str*): UID da fonte relacional.
  - `sql_query` (*str*): Comando SQL (apenas `SELECT` ou `WITH`).
- **Retorno:** Linhas e colunas resultantes formatadas em tabela.

### 037. `grafana_executar_consulta_painel`
- **Para que serve:** Executa exatamente as consultas configuradas em um painel de dashboard já existente, retornando os dados renderizados.
- **Quando usar:** Para verificar o valor atual que determinado gráfico está exibindo sem precisar reconstruir a query.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `id_painel` (*int*): ID do painel.
- **Retorno:** Dados atuais do painel.

### 038. `grafana_comparar_metricas_periodos`
- **Para que serve:** Compara a mesma métrica entre dois períodos temporais distintos (ex: "hoje vs ontem" ou "esta semana vs semana passada").
- **Quando usar:** Avaliação de impacto de deploys, comparativos de tráfego e pós-incidentes.
- **Parâmetros:**
  - `datasource_uid` (*str*): UID da fonte de dados.
  - `query` (*str*): Consulta de métrica.
  - `periodo_atual` (*str*, padrão `"now-1h"`): Janela recente.
  - `periodo_comparacao` (*str*, padrão `"now-25h"`): Janela passada.
- **Retorno:** Delta percentual de variação, valores médios e pico de ambos os períodos.

### 039. `grafana_analisar_tendencias_metricas`
- **Para que serve:** Analisa o comportamento histórico de uma métrica calculando inclinação, média, desvio padrão e tendência de crescimento.
- **Quando usar:** Planejamento de capacidade e alertas preventivos de exaustão de recursos.
- **Parâmetros:**
  - `datasource_uid` (*str*): UID da fonte.
  - `query` (*str*): Expressão da métrica.
  - `periodo` (*str*, padrão `"7d"`): Janela de análise.
- **Retorno:** Estatísticas descritivas e tendência (`estável`, `crescimento`, `degradação`).

### 040. `grafana_detectar_anomalias_metricas`
- **Para que serve:** Identifica valores fora do padrão estatístico esperado (*outliers*) aplicando cálculo de desvio padrão (Z-Score).
- **Quando usar:** Detecção precoce de incidentes, picos inesperados e comportamentos incomuns.
- **Parâmetros:**
  - `datasource_uid` (*str*): UID da fonte.
  - `query` (*str*): Expressão da métrica.
  - `sensibilidade` (*float*, padrão `3.0`): Número de desvios padrão para considerar anomalia.
- **Retorno:** Lista de pontos anômalos com timestamps e severidade.

---

## Categoria D: Logs, Traces e Observabilidade (041 a 050)

### 041. `grafana_pesquisar_logs`
- **Para que serve:** Pesquisa linhas de log em fontes Loki com suporte a expressões de filtro de texto e rótulos.
- **Quando usar:** Análise de erros de aplicações e auditoria de eventos operacionais.
- **Parâmetros:**
  - `logql` (*str*): Expressão LogQL (ex: `{app="checkout"} |= "panic"`).
  - `datasource_uid` (*str | None*): UID da fonte Loki.
  - `de` (*str*, padrão `"now-1h"`): Janela inicial.
  - `ate` (*str*, padrão `"now"`): Janela final.
  - `limite` (*int*, padrão `100`): Quantidade máxima de linhas.
- **Retorno:** Entradas de log ordenadas com timestamp, stream e mensagem.

### 042. `grafana_identificar_padroes_erro`
- **Para que serve:** Agrupa e classifica automaticamente mensagens de erro em logs por frequência e padrão de ocorrência.
- **Quando usar:** Diagnóstico rápido de grandes volumes de logs de falhas.
- **Parâmetros:**
  - `logql` (*str*): Expressão de filtro.
  - `datasource_uid` (*str | None*): UID da fonte.
  - `limite_linhas` (*int*, padrão `500`): Amostra de logs a analisar.
- **Retorno:** Tabela de padrões de erro mais frequentes e percentual de impacto.

### 043. `grafana_identificar_requisicoes_lentas`
- **Para que serve:** Localiza spans de rastreamento com duração acima de um limiar especificado.
- **Quando usar:** Resolução de gargalos de desempenho e otimização de endpoints lentos.
- **Parâmetros:**
  - `datasource_uid` (*str*): UID da fonte Tempo.
  - `servico` (*str*): Nome do serviço monitorado.
  - `limiar_ms` (*int*, padrão `1000`): Duração mínima em milissegundos para considerar lento.
- **Retorno:** Lista de traces lentos com endpoint, latência e identificador de trace.

### 044. `grafana_obter_detalhes_trace`
- **Para que serve:** Recupera a árvore completa de spans de uma transação distribuída pelo ID do trace.
- **Quando usar:** Visualização detalhada do caminho percorrido por uma requisição que falhou ou demorou.
- **Parâmetros:**
  - `trace_id` (*str*): Identificador hexadecimal do trace.
  - `datasource_uid` (*str | None*): UID da fonte Tempo.
- **Retorno:** Árvore hierárquica de spans, serviços envolvidos, tempos e logs embutidos.

### 045. `grafana_comparar_traces`
- **Para que serve:** Compara um trace de requisição bem-sucedida contra um trace de requisição lenta ou com falha.
- **Quando usar:** Para isolar exatamente qual microsserviço ou operação adicionou latência.
- **Parâmetros:**
  - `trace_id_a` (*str*): ID do primeiro trace (ex: baseline normal).
  - `trace_id_b` (*str*): ID do segundo trace (ex: trace degradado).
- **Retorno:** Comparativo diferencial de duração por operação.

### 046. `grafana_explorar_atributos_trace`
- **Para que serve:** Lista atributos, tags de span e valores mais comuns em traces de um serviço.
- **Quando usar:** Descoberta de tags indexadas (ex: `http.status_code`, `db.statement`).
- **Parâmetros:**
  - `servico` (*str*): Nome do serviço.
  - `datasource_uid` (*str | None*): UID da fonte Tempo.
- **Retorno:** Catálogo de tags disponíveis.

### 047. `grafana_correlacionar_logs_metricas_traces`
- **Para que serve:** Realiza correlação 360° combinando métricas, logs e traces de uma mesma janela de tempo para um serviço.
- **Quando usar:** Investigação profunda de incidentes onde métricas apontam anomalia, logs apontam stacktraces e traces apontam o componente causador.
- **Parâmetros:**
  - `servico` (*str*): Nome do serviço ou aplicação.
  - `janela_tempo` (*str*, padrão `"30m"`): Período a correlacionar.
- **Retorno:** Visão analítica unificada com os 3 pilares da observabilidade correlacionados.

### 048. `grafana_investigar_servico`
- **Para que serve:** Conduz varredura diagnóstica completa no serviço (taxa de erro, throughput, latência e logs recentes).
- **Quando usar:** Triagem rápida de chamados de suporte técnico.
- **Parâmetros:**
  - `nome_servico` (*str*): Nome do serviço monitorado.
- **Retorno:** Diagnóstico executivo com status de saúde do serviço.

### 049. `grafana_diagnosticar_degradacao`
- **Para que serve:** Avalia se o ambiente apresenta degradação em cascata nos últimos minutos e aponta o provável foco inicial.
- **Quando usar:** Quando múltiplos alertas de diferentes serviços disparam simultaneamente.
- **Parâmetros:**
  - `janela_minutos` (*int*, padrão `15`): Período de análise.
- **Retorno:** Relatório de diagnóstico apontando causa raiz provável e impacto.

### 050. `grafana_gerar_linha_tempo_incidente`
- **Para que serve:** Constrói uma linha do tempo cronológica com todos os eventos, anotações e picos ocorridos durante uma falha.
- **Quando usar:** Elaboração de pós-mortem e relatórios de RCA (Root Cause Analysis).
- **Parâmetros:**
  - `inicio` (*str*): Timestamp ou termo inicial (ex: `"now-2h"`).
  - `fim` (*str*, padrão `"now"`): Timestamp final.
- **Retorno:** Linha do tempo sequencial dos eventos detectados.

---

## Categoria E: Alertas e Notificações (051 a 060)

### 051. `grafana_listar_regras_alerta`
- **Para que serve:** Lista todas as regras de alerta configuradas no Grafana Unified Alerting.
- **Quando usar:** Auditoria de alertas existentes e verificação de condições de disparo.
- **Parâmetros:** Nenhum.
- **Retorno:** Lista de regras com `uid`, `title`, `folderUID`, `condition`, `labels`.

### 052. `grafana_obter_regra_alerta`
- **Para que serve:** Consulta a definição completa, queries e thresholds de uma regra de alerta específica.
- **Quando usar:** Para inspecionar expressões e limites de disparo antes de alterar uma regra.
- **Parâmetros:**
  - `uid_regra` (*str*): UID da regra de alerta.
- **Retorno:** Detalhes técnicos e metadados da regra.

### 053. `grafana_criar_regra_alerta`
- **Para que serve:** Cria uma nova regra de alerta no Grafana Alerting.
- **Quando usar:** Provisionamento automatizado de alarmes operacionais.
- **Parâmetros:**
  - `regra_payload` (*dict*): Estrutura validada da regra (`title`, `ruleGroup`, `data`, `condition`, etc.).
- **Retorno:** UID da regra de alerta criada.

### 054. `grafana_atualizar_regra_alerta`
- **Para que serve:** Modifica os limiares, expressões ou labels de uma regra existente.
- **Quando usar:** Ajuste de sensibilidade de alertas para mitigar falsos positivos.
- **Parâmetros:**
  - `uid_regra` (*str*): UID da regra a modificar.
  - `regra_payload` (*dict*): Nova definição.
- **Retorno:** Confirmação da atualização.

### 055. `grafana_excluir_regra_alerta`
- **Para que serve:** Remove uma regra de alerta da instância.
- **Quando usar:** Limpeza de alarmes descontinuados (requer token de aprovação).
- **Parâmetros:**
  - `uid_regra` (*str*): UID da regra.
  - `token_aprovacao` (*str | None*): Token HMAC.
- **Retorno:** Confirmação de exclusão.

### 056. `grafana_listar_instancias_alerta`
- **Para que serve:** Lista os alertas que estão atualmente disparados (*firing*), pendentes (*pending*) ou normais (*normal*).
- **Quando usar:** Monitoramento em tempo real do NOC e telas de operação.
- **Parâmetros:** Nenhum.
- **Retorno:** Lista de instâncias com estado, rótulos e horário do acionamento.

### 057. `grafana_gerenciar_politicas_notificacao`
- **Para que serve:** Consulta ou atualiza a árvore de políticas de roteamento de notificações do Grafana Alerting.
- **Quando usar:** Para definir para onde alertas críticos, de aviso ou de times específicos devem ser enviados.
- **Parâmetros:**
  - `acao` (*str*, padrão `"consultar"`): `"consultar"` ou `"atualizar"`.
  - `politica_dados` (*dict | None*): Árvore de rotas e agrupamentos.
- **Retorno:** Estrutura da árvore de roteamento ativa.

### 058. `grafana_gerenciar_pontos_contato`
- **Para que serve:** Lista, cadastra ou testa pontos de contato (*contact points*) como Slack, Telegram, Webhook, PagerDuty, Email.
- **Quando usar:** Configuração de novos canais de notificação para equipes.
- **Parâmetros:**
  - `acao` (*str*, padrão `"listar"`): `"listar"`, `"criar"` ou `"testar"`.
  - `ponto_contato_dados` (*dict | None*): Dados do canal (`name`, `type`, `settings`).
- **Retorno:** Lista de pontos de contato ou resultado do teste de entrega.

### 059. `grafana_gerenciar_silenciamentos`
- **Para que serve:** Cria, consulta ou remove silenciamentos temporários de alertas durante janelas de manutenção.
- **Quando usar:** Antes de realizar paradas programadas de servidores para evitar flood de notificações.
- **Parâmetros:**
  - `acao` (*str*, padrão `"listar"`): `"listar"`, `"criar"` ou `"remover"`.
  - `silenciamento_dados` (*dict | None*): `matchers`, `startsAt`, `endsAt`, `comment`, `silence_id`.
- **Retorno:** ID do silenciamento ativo ou confirmação de remoção.

### 060. `grafana_diagnosticar_alertas`
- **Para que serve:** Audita a saúde do sistema de alertas, detectando regras em flapping, regras sem ponto de contato associado e notificações com falha de envio.
- **Quando usar:** Revisão mensal de observabilidade e confiabilidade de alertas.
- **Parâmetros:** Nenhum.
- **Retorno:** Relatório com métricas de ruído, alertas fantasmas e recomendações de ajuste.

---

## Categoria F: Pastas, Tags e Anotações (061 a 070)

### 061. `grafana_listar_pastas`
- **Para que serve:** Lista todas as pastas de organização de dashboards.
- **Quando usar:** Descoberta de estrutura departamental de dashboards.
- **Parâmetros:**
  - `limite` (*int*, padrão `100`): Máximo de registros.
  - `pagina` (*int*, padrão `1`): Página atual.
- **Retorno:** Lista de pastas com `uid`, `title`, `url`.

### 062. `grafana_criar_pasta`
- **Para que serve:** Cria uma nova pasta no Grafana para agrupar dashboards de um projeto ou equipe.
- **Quando usar:** Provisionamento de novos departamentos na plataforma.
- **Parâmetros:**
  - `titulo` (*str*): Nome da nova pasta.
  - `uid` (*str | None*): UID customizado opcional.
- **Retorno:** UID e metadados da pasta criada.

### 063. `grafana_atualizar_pasta`
- **Para que serve:** Renomeia uma pasta existente.
- **Quando usar:** Reestruturação e padronização de nomenclatura.
- **Parâmetros:**
  - `uid` (*str*): UID da pasta.
  - `novo_titulo` (*str*): Novo nome.
- **Retorno:** Metadados da pasta atualizada.

### 064. `grafana_excluir_pasta`
- **Para que serve:** Exclui uma pasta e seus dashboards contidos (requer aprovação administrativa).
- **Quando usar:** Limpeza definitiva de projetos arquivados.
- **Parâmetros:**
  - `uid` (*str*): UID da pasta.
  - `token_aprovacao` (*str | None*): Token HMAC de confirmação.
- **Retorno:** Confirmação de exclusão.

### 065. `grafana_mover_dashboard`
- **Para que serve:** Transfere um dashboard da pasta atual para outra pasta de destino.
- **Quando usar:** Organização e movimentação de dashboards criados na pasta Geral.
- **Parâmetros:**
  - `uid_dashboard` (*str*): UID do dashboard.
  - `nova_pasta_id` (*int*): ID numérico da pasta de destino (`0` para pasta Geral).
- **Retorno:** Confirmação de movimentação.

### 066. `grafana_listar_tags`
- **Para que serve:** Retorna todas as tags utilizadas nos dashboards e a contagem de uso de cada uma.
- **Quando usar:** Padronização de governança e categorização de recursos.
- **Parâmetros:** Nenhum.
- **Retorno:** Lista de tags com contagem.

### 067. `grafana_pesquisar_recursos`
- **Para que serve:** Busca unificada em toda a instância por dashboards, pastas e painéis em um único comando.
- **Quando usar:** Localização rápida de qualquer ativo na plataforma por palavra-chave.
- **Parâmetros:**
  - `consulta` (*str*): Termo de busca.
  - `tipo` (*str | None*): `"dash-folder"`, `"dash-db"`, etc.
- **Retorno:** Lista consolidada de recursos encontrados.

### 068. `grafana_gerar_link_explore`
- **Para que serve:** Constrói uma URL direta para a interface do Grafana Explore com a query de métrica, log ou trace pré-carregada.
- **Quando usar:** Para enviar ao operador uma página pronta para investigação livre com um único clique.
- **Parâmetros:**
  - `datasource_uid` (*str*): UID da fonte.
  - `query` (*str*): Consulta a carregar no Explore.
  - `de` (*str*, padrão `"now-1h"`): Início.
  - `ate` (*str*, padrão `"now"`): Fim.
- **Retorno:** URL web para a aba Explore.

### 069. `grafana_gerenciar_snapshots`
- **Para que serve:** Cria ou lista snapshots públicos/internos de dashboards congelados em um instante no tempo.
- **Quando usar:** Compartilhamento seguro de métricas com terceiros sem conceder acesso à fonte de dados.
- **Parâmetros:**
  - `acao` (*str*, padrão `"listar"`): `"listar"` ou `"criar"`.
  - `snapshot_dados` (*dict | None*): Parâmetros do snapshot (`dashboard`, `name`, `expires`).
- **Retorno:** Lista de snapshots ou URL do snapshot gerado.

### 070. `grafana_gerenciar_anotacoes`
- **Para que serve:** Lista ou registra anotações manuais/automáticas na linha do tempo dos dashboards (ex: "Deploy v2.4.0 aplicado", "Incidente iniciado").
- **Quando usar:** Marcar eventos na linha do tempo para correlacionar alterações com oscilações de métricas.
- **Parâmetros:**
  - `acao` (*str*, padrão `"listar"`): `"listar"` ou `"criar"`.
  - `anotacao_dados` (*dict | None*): `text`, `tags`, `time`, `dashboardUID`, `panelId`.
- **Retorno:** ID da anotação criada ou lista de anotações registradas.

---

## Categoria G: Relatórios e Renderização (071 a 080)

### 071. `grafana_gerar_relatorio_executivo`
- **Para que serve:** Consolida a saúde da infraestrutura, total de fontes de dados, dashboards monitorados e regras de alerta em um documento executivo formatado (PDF, XLSX, CSV, JSON ou Markdown).
- **Quando usar:** Reuniões de alinhamento com a diretoria, relatórios semanais de SRE e prestação de contas.
- **Parâmetros:**
  - `titulo` (*str*, padrão `"Relatório Executivo de Observabilidade Grafana"`): Cabeçalho do documento.
  - `periodo` (*str*, padrão `"7d"`): Janela de análise.
  - `formato` (*str*, padrão `"pdf"`): Formato desejado (`pdf`, `xlsx`, `csv`, `json`, `markdown`).
  - `incluir_graficos` (*bool*, padrão `True`): Inclusão de indicadores visuais.
- **Retorno:** Caminho do arquivo exportado no disco e metadados de execução.

### 072. `grafana_gerar_relatorio_disponibilidade`
- **Para que serve:** Gera relatório técnico de disponibilidade de serviços, conformidade de SLA e tempos de parada (*downtime*).
- **Quando usar:** Fechamento mensal de SLA contratual e auditoria de uptime.
- **Parâmetros:**
  - `servicos_ou_tags` (*list[str] | None*): Lista de serviços a incluir.
  - `periodo` (*str*, padrão `"30d"`): Janela de apuração.
  - `formato` (*str*, padrão `"pdf"`): Formato de saída.
- **Retorno:** Caminho do documento gerado e sumário de conformidade.

### 073. `grafana_gerar_relatorio_desempenho`
- **Para que serve:** Consolida métricas de latência média, p95, p99, taxas de erro e consumo de hardware no período.
- **Quando usar:** Análise de performance pré e pós migrações de sistemas.
- **Parâmetros:**
  - `dashboard_uid` (*str | None*): UID do dashboard de referência.
  - `periodo` (*str*, padrão `"24h"`): Janela analisada.
  - `formato` (*str*, padrão `"pdf"`): Formato de saída.
- **Retorno:** Arquivo de relatório de performance gerado.

### 074. `grafana_gerar_relatorio_alertas`
- **Para que serve:** Emite relatório com o histórico de alarmes disparados, severidade, tempo de duração e regras mais acionadas.
- **Quando usar:** Identificação de fadiga de alertas e regras ruidosas.
- **Parâmetros:**
  - `estado` (*str | None*): Filtrar por estado.
  - `periodo` (*str*, padrão `"7d"`): Janela de análise.
  - `formato` (*str*, padrão `"pdf"`): Formato do relatório.
- **Retorno:** Arquivo consolidado de alertas emitido.

### 075. `grafana_gerar_relatorio_incidentes`
- **Para que serve:** Gera relatório de resposta a incidentes operacionais contendo MTTD, MTTR e resoluções aplicadas.
- **Quando usar:** Governança de incidentes e revisão operacional mensal.
- **Parâmetros:**
  - `periodo` (*str*, padrão `"30d"`): Janela analisada.
  - `formato` (*str*, padrão `"pdf"`): Formato de saída.
- **Retorno:** Arquivo do relatório de incidentes.

### 076. `grafana_gerar_relatorio_capacidade`
- **Para que serve:** Gera relatório de planejamento de capacidade (*Capacity Planning*) com projeção de crescimento e risco de esgotamento de recursos para os próximos 90 dias.
- **Quando usar:** Orçamento de infraestrutura e prevenção de saturação de discos e memória.
- **Parâmetros:**
  - `recursos` (*list[str] | None*): Lista de recursos a analisar (CPU, RAM, Disco, Banda).
  - `periodo` (*str*, padrão `"30d"`): Base histórica utilizada.
  - `formato` (*str*, padrão `"pdf"`): Formato de exportação.
- **Retorno:** Arquivo de planejamento de capacidade salvo no disco.

### 077. `grafana_renderizar_painel`
- **Para que serve:** Gera a URL do endpoint de renderização do Grafana Image Renderer para download de imagem PNG de um painel individual.
- **Quando usar:** Para embutir capturas de gráficos em mensagens do Slack, Telegram ou e-mails.
- **Parâmetros:**
  - `dashboard_uid` (*str*): UID do dashboard.
  - `panel_id` (*int*): ID do painel.
  - `largura` (*int*, padrão `1000`): Largura em pixels.
  - `altura` (*int*, padrão `500`): Altura em pixels.
  - `de` (*str*, padrão `"now-6h"`): Início.
  - `ate` (*str*, padrão `"now"`): Fim.
- **Retorno:** URL de renderização direta da imagem PNG.

### 078. `grafana_renderizar_dashboard`
- **Para que serve:** Gera a URL para captura de tela completa do dashboard em alta resolução via serviço de renderização.
- **Quando usar:** Geração de snapshots visuais para relatórios impressos.
- **Parâmetros:**
  - `dashboard_uid` (*str*): UID do dashboard.
  - `largura` (*int*, padrão `1920`): Largura em pixels.
  - `altura` (*int*, padrão `1080`): Altura em pixels.
  - `de` (*str*, padrão `"now-6h"`): Início.
  - `ate` (*str*, padrão `"now"`): Fim.
- **Retorno:** URL de renderização do dashboard.

### 079. `grafana_exportar_relatorio_pdf`
- **Para que serve:** Exporta dados analíticos customizados fornecidos pelo agente diretamente para um documento PDF corporativo diagramado profissionalmente.
- **Quando usar:** Criação sob demanda de relatórios técnicos arbitrários em PDF.
- **Parâmetros:**
  - `titulo` (*str*): Título principal do relatório.
  - `resumo` (*str*): Texto do sumário executivo.
  - `cabecalhos` (*list[str]*): Lista de títulos das colunas da tabela.
  - `linhas` (*list[list]*): Dados tabulares linha a linha.
  - `arquivo_saida` (*str | None*): Caminho customizado opcional de saída.
- **Retorno:** Caminho do arquivo PDF gerado e total de linhas registradas.

### 080. `grafana_exportar_relatorio_csv_excel`
- **Para que serve:** Exporta dados tabulares para planilhas Excel formatadas (`.xlsx`) ou arquivos separados por vírgula (`.csv`).
- **Quando usar:** Exportação de dados brutos para contabilidade, auditorias externas ou planilhas de terceiros.
- **Parâmetros:**
  - `titulo` (*str*): Título da planilha.
  - `cabecalhos` (*list[str]*): Nomes das colunas.
  - `linhas` (*list[list]*): Matriz de dados.
  - `formato` (*str*, padrão `"xlsx"`): `"xlsx"` ou `"csv"`.
  - `arquivo_saida` (*str | None*): Caminho de saída.
- **Retorno:** Caminho do arquivo salvo no disco.

---

## Categoria H: Incidentes, SLOs e OnCall (081 a 090)

### 081. `grafana_listar_incidentes`
- **Para que serve:** Consulta a lista de incidentes operacionais ativos ou resolvidos no Grafana Incident (ou anotações globais de incidentes).
- **Quando usar:** Triagem de crises operacionais e acompanhamento do status de incidentes em aberto.
- **Parâmetros:**
  - `status` (*str | None*): Filtrar por status (`active`, `resolved`, etc.).
  - `limit` (*int*, padrão `50`): Quantidade máxima retornada.
- **Retorno:** Lista de incidentes com ID, título, severidade e responsáveis.

### 082. `grafana_criar_incidente`
- **Para que serve:** Declara formalmente um novo incidente operacional, notificando os times e marcando a linha do tempo.
- **Quando usar:** No momento em que uma indisponibilidade ou severa degradação for confirmada.
- **Parâmetros:**
  - `titulo` (*str*): Nome resumido do incidente.
  - `severidade` (*str*, padrão `"major"`): Gravidade (`minor`, `major`, `critical`).
  - `descricao` (*str | None*): Detalhamento do impacto operacional observado.
  - `rotulos` (*dict | None*): Labels de contexto (serviço, time, cliente).
- **Retorno:** Identificador do incidente criado e status.

### 083. `grafana_obter_incidente`
- **Para que serve:** Consulta detalhes, linha do tempo e status de um incidente pelo seu ID.
- **Quando usar:** Acompanhamento durante o processo de mitigação.
- **Parâmetros:**
  - `incidente_id` (*str*): Identificador do incidente.
- **Retorno:** Detalhes completos do incidente.

### 084. `grafana_atualizar_incidente`
- **Para que serve:** Altera o status do incidente (ex: `investigating` -> `mitigated` -> `resolved`) e adiciona resumos.
- **Quando usar:** A cada mudança significativa na resposta ao incidente.
- **Parâmetros:**
  - `incidente_id` (*str*): ID do incidente.
  - `status` (*str | None*): Novo status.
  - `resumo` (*str | None*): Resumo das ações tomadas.
- **Retorno:** Confirmação de atualização do incidente.

### 085. `grafana_adicionar_atividade_incidente`
- **Para que serve:** Adiciona notas, comentários, evidências ou ações tomadas na linha do tempo do incidente.
- **Quando usar:** Documentação em tempo real durante a crise operacional.
- **Parâmetros:**
  - `incidente_id` (*str*): ID do incidente.
  - `mensagem` (*str*): Conteúdo do apontamento.
- **Retorno:** Confirmação de registro da atividade.

### 086. `grafana_gerenciar_agendas_oncall`
- **Para que serve:** Consulta ou configura as escalas de plantão e rotas de plantonistas no Grafana OnCall.
- **Quando usar:** Verificação de quem é o engenheiro de sobreaviso ativo no momento.
- **Parâmetros:**
  - `acao` (*str*, padrão `"listar"`): `"listar"` ou `"criar"`.
  - `agenda_dados` (*dict | None*): Dados da escala.
- **Retorno:** Escalas de plantonistas ativas e fuso horário.

### 087. `grafana_consultar_grupos_alerta_oncall`
- **Para que serve:** Consulta grupos de alerta roteados para a fila de atendimento do plantão OnCall.
- **Quando usar:** Visualização de chamados pendentes de reconhecimento pelo plantonista.
- **Parâmetros:** Nenhum.
- **Retorno:** Grupos de alerta pendentes de atendimento.

### 088. `grafana_consultar_slos`
- **Para que serve:** Consulta a lista de objetivos de nível de serviço (SLOs) e conformidade de SLIs.
- **Quando usar:** Acompanhamento da meta contratual de disponibilidade e latência.
- **Parâmetros:**
  - `nome_ou_tag` (*str | None*): Filtro por nome ou tag.
- **Retorno:** Lista de SLOs com meta percentual e valor apurado no período.

### 089. `grafana_analisar_orcamento_erro`
- **Para que serve:** Calcula matematicamente o consumo do orçamento de erro (*Error Budget*) e a taxa de queima (*Burn Rate*), indicando se há risco de violação de SLO.
- **Quando usar:** Para decidir se novos deploys devem ser congelados em função de instabilidade recente.
- **Parâmetros:**
  - `slo_id_ou_nome` (*str*): Nome ou identificador do SLO analisado.
  - `periodo` (*str*, padrão `"30d"`): Janela de tolerância.
- **Retorno:** Percentual de orçamento consumido, tempo restante de tolerância e taxa de queima.

### 090. `grafana_gerar_resumo_pos_incidente`
- **Para que serve:** Gera automaticamente a minuta estruturada de relatório de pós-mortem em Markdown com resumo, linha do tempo dos fatos, causa raiz e planos de ação.
- **Quando usar:** Imediatamente após a resolução de um incidente operacional relevante.
- **Parâmetros:**
  - `incidente_id` (*str*): ID do incidente.
  - `formato` (*str*, padrão `"markdown"`): Formato desejado.
- **Retorno:** Documento completo de RCA / Post-Mortem.

---

## Categoria I: Administração, Governança e Auditoria (091 a 100)

### 091. `grafana_obter_informacoes_instancia`
- **Para que serve:** Retorna a versão exata do Grafana, commit de compilação, integridade do banco interno e organização conectada.
- **Quando usar:** Verificação de compatibilidade e inventário de versões.
- **Parâmetros:** Nenhum.
- **Retorno:** Objeto com `versao`, `commit`, `status_banco`, `organizacao_atual`.

### 092. `grafana_listar_organizacoes`
- **Para que serve:** Lista todas as organizações (*orgs*) configuradas na instância Grafana multitenant.
- **Quando usar:** Governança e auditoria de ambientes compartilhados entre clientes ou subsidiárias.
- **Parâmetros:** Nenhum.
- **Retorno:** Lista de organizações cadastradas.

### 093. `grafana_listar_usuarios`
- **Para que serve:** Lista os usuários membros da organização atual, seus papéis (*roles*) e e-mails.
- **Quando usar:** Auditoria de acessos e desligamentos de colaboradores.
- **Parâmetros:**
  - `limit` (*int*, padrão `50`): Quantidade de usuários por página.
  - `page` (*int*, padrão `1`): Número da página.
- **Retorno:** Lista de usuários cadastrados com login e permissão.

### 094. `grafana_listar_equipes`
- **Para que serve:** Lista equipes e times de trabalho (*teams*) configurados na organização.
- **Quando usar:** Identificação de grupos de usuários para concessão de permissões em dashboards.
- **Parâmetros:**
  - `query` (*str | None*): Termo de filtro para nomes de equipes.
- **Retorno:** Lista de equipes com IDs e membros.

### 095. `grafana_gerenciar_equipes`
- **Para que serve:** Cria, atualiza ou exclui equipes no Grafana com controle de permissão e confirmação em dois passos para exclusões.
- **Quando usar:** Provisionamento de novos times na plataforma de observabilidade.
- **Parâmetros:**
  - `acao` (*str*, padrão `"consultar"`): `"consultar"`, `"criar"`, `"atualizar"` ou `"excluir"`.
  - `team_id` (*int | None*): ID da equipe.
  - `nome` (*str | None*): Nome da equipe.
  - `email` (*str | None*): E-mail de contato da equipe.
  - `token_aprovacao` (*str | None*): Token exigido para exclusão.
- **Retorno:** Resultado da operação cadastral.

### 096. `grafana_consultar_permissoes`
- **Para que serve:** Consulta a lista de controle de acesso (ACL) de um dashboard ou pasta específica.
- **Quando usar:** Auditoria de segurança para verificar quem tem permissão de visualização ou edição em determinado recurso.
- **Parâmetros:**
  - `tipo_recurso` (*str*): `"dashboard"` ou `"folder"`.
  - `recurso_id` (*str*): UID do recurso.
- **Retorno:** Lista de permissões associadas a usuários, equipes e funções.

### 097. `grafana_gerenciar_permissoes_dashboard`
- **Para que serve:** Modifica ou define permissões de acesso (Viewer, Editor, Admin) de um dashboard.
- **Quando usar:** Restrição de visualização de dashboards com dados sensíveis para equipes específicas.
- **Parâmetros:**
  - `dashboard_uid` (*str*): UID do dashboard.
  - `itens_permissao` (*list[dict]*): Lista de permissões (`role`, `teamId`, `userId`, `permission`).
- **Retorno:** Confirmação da aplicação das permissões.

### 098. `grafana_gerenciar_permissoes_pasta`
- **Para que serve:** Define a lista de permissões herdadas por todos os dashboards contidos em uma pasta.
- **Quando usar:** Governança departamental (ex: apenas o time de finanças edita a pasta Financeiro).
- **Parâmetros:**
  - `folder_uid` (*str*): UID da pasta.
  - `itens_permissao` (*list[dict]*): Permissões a atribuir.
- **Retorno:** Confirmação da aplicação das permissões na pasta.

### 099. `grafana_auditar_configuracoes`
- **Para que serve:** Executa uma auditoria abrangente de segurança, conformidade e boas práticas na instância (checando versão, fontes de dados desprotegidas, dashboards desorganizados na pasta raiz e permissões).
- **Quando usar:** Rotinas semanais de segurança, auditorias de conformidade SOC2/ISO27001 e preparação de ambientes.
- **Parâmetros:** Nenhum.
- **Retorno:** Relatório detalhado com pontuação de conformidade (0 a 100), lista de conformidades e recomendações corretivas.

### 100. `grafana_testar_conexao`
- **Para que serve:** Testa a conectividade imediata com o servidor Grafana, valida a autenticidade do token/credencial, mede a latência em milissegundos e retorna o diagnóstico completo.
- **Quando usar:** Na inicialização de agentes de IA e no início de qualquer fluxo de trabalho para certificar que a instância está ativa e respondendo.
- **Parâmetros:** Nenhum.
- **Retorno:** Objeto com `status`, `versao_grafana`, `latencia_ms`, `autenticacao`, `datasources_detectadas` e modo de segurança.
