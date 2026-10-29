# 📊 Motor de Relatórios Corporativos Multi-Formato

O **Grafana MCP Server** inclui um motor de relatórios profissionais capaz de consolidar métricas, alertas, disponibilidade de serviços (SLAs) e capacidade operacional em documentos formatados prontos para distribuição executiva.

---

## 1. Formatos Suportados

| Formato | Biblioteca | Extensão | Finalidade Principal |
| :--- | :--- | :--- | :--- |
| **PDF** | ReportLab | `.pdf` | Relatórios executivos diagramados com sumários, tabelas estilizadas e cabeçalhos. |
| **Excel** | OpenPyXL | `.xlsx` | Planilhas com múltiplas abas, colunas auto-ajustadas e dados analíticos. |
| **CSV** | Nativo Python | `.csv` | Exportações tabulares para ingestão em data lakes ou ferramentas de BI. |
| **JSON** | Nativo Python | `.json` | Integrações automatizadas entre sistemas e esteiras CI/CD. |
| **Markdown** | Nativo Python | `.md` | Documentação técnica, notas de pós-mortem e documentação interna. |

---

## 2. Tipos de Relatórios Nativos

### 1. Relatório Executivo de Observabilidade
- **Ferramenta:** `grafana_gerar_relatorio_executivo`
- **Conteúdo:** Estado global da instância, quantidade de fontes de dados saudáveis, volume de dashboards e inventário de alertas.
- **Público-alvo:** CTO, Diretores de TI, Gerentes de Engenharia.

### 2. Relatório de Disponibilidade e SLA
- **Ferramenta:** `grafana_gerar_relatorio_disponibilidade`
- **Conteúdo:** Percentual de disponibilidade por serviço, tempo acumulado de indisponibilidade, conformidade contra a meta contratual.
- **Público-alvo:** Clientes, Gestão de Contratos, SREs.

### 3. Relatório de Desempenho Operacional
- **Ferramenta:** `grafana_gerar_relatorio_desempenho`
- **Conteúdo:** Latência média, p95 e p99 da API, taxas de requisições por segundo (QPS) e consumo de hardware.
- **Público-alvo:** Arquitetos de Software, Desenvolvedores e Engenheiros de Performance.

### 4. Relatório de Planejamento de Capacidade (Capacity Planning)
- **Ferramenta:** `grafana_gerar_relatorio_capacidade`
- **Conteúdo:** Projeção linear de consumo de armazenamento, memória e CPU para os próximos 90 dias, com estimativa de risco de saturação.
- **Público-alvo:** Administradores de Infraestrutura, FinOps e Gestores de Capacidade.

### 5. Relatório de Auditoria de Alertas
- **Ferramenta:** `grafana_gerar_relatorio_alertas`
- **Conteúdo:** Alertas mais frequentes, regras com ruído excessivo, distribuição por severidade.
- **Público-alvo:** Equipes de NOC e SOC.

---

## 3. Diretório de Saída dos Relatórios

Por padrão, todos os relatórios são gravados no diretório local configurado na variável `MCP_REPORT_OUTPUT_DIR` (padrão: `./reports_output/`).
Cada arquivo recebe um prefixo com o tipo do relatório e um carimbo de data/hora no padrão `YYYYMMDD_HHMMSS`.
Exemplo:
`./reports_output/relatorio_executivo_20261029_101013.pdf`
