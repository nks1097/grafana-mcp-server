# 🏛️ Arquitetura do Grafana MCP Server

O **Grafana MCP Server** foi projetado seguindo os princípios de alta coesão, baixo acoplamento, observabilidade e segurança defensiva para suportar operação em ambientes corporativos de grande porte.

---

## 1. Diagrama Arquitetural Geral

```mermaid
flowchart TD
    Client["Agente de IA / Cliente MCP\n(Claude, Antigravity IDE, Cursor)"] -->|STDIO / SSE| FastMCPServer["Servidor FastMCP / MCPServer\n(grafana_mcp.server)"]

    subgraph CoreEngine["Núcleo do Servidor (Core Engine)"]
        FastMCPServer --> ToolRouter["Roteador das 100 Ferramentas\n(tools/)"]
        FastMCPServer --> PromptRouter["Prompts Especializados"]
        FastMCPServer --> RBAC["Gerenciador RBAC\n(authorization.py)"]
        FastMCPServer --> HMAC["Gerenciador de Políticas HMAC\n(policies.py)"]
        FastMCPServer --> AuditLog["Trilha de Auditoria JSONL\n(audit.py)"]
    end

    subgraph Engines["Motores Especializados"]
        ToolRouter --> DashBuilder["Dashboard Builder (9 Etapas)\n(dashboard_builder.py)"]
        ToolRouter --> QueryPlanner["Query Planner\n(query_planner.py)"]
        ToolRouter --> QueryValidator["Query Validator\n(query_validation.py)"]
        ToolRouter --> DashValidator["Dashboard Schema Validator\n(dashboard_validator.py)"]
        ToolRouter --> ReportEngine["Motor de Relatórios\n(reports/generator.py)"]
    end

    subgraph ClientLayer["Camada de Integração HTTP"]
        DashBuilder --> GrafanaClient["GrafanaClient Assíncrono\n(client.py)"]
        QueryPlanner --> GrafanaClient
        ToolRouter --> GrafanaClient
        GrafanaClient -->|HTTPX Connection Pool| TargetGrafana["Instância Grafana API\n(v9 / v10 / v11 / v12 / v13)"]
    end

    subgraph DataOutputs["Exportações e Destinos"]
        ReportEngine --> PDF["Relatório PDF Corporativo\n(ReportLab)"]
        ReportEngine --> XLSX["Planilha Excel (.xlsx)\n(OpenPyXL)"]
        ReportEngine --> CSV["Arquivo CSV / JSON"]
    end
```

---

## 2. Camadas do Sistema

### 1. Camada de Apresentação (MCP Interface)
- Implementa o protocolo MCP utilizando a biblioteca oficial `mcp` (v2.x / MCPServer).
- Oferece suporte nativo a dois modos de transporte:
  - **`stdio`:** Comunicação via pipes padrão para integração com IDEs locais (Claude Desktop, Antigravity IDE, Cursor).
  - **`sse`:** Transporte HTTP Server-Sent Events para execução em rede, Kubernetes ou contêineres Docker.

### 2. Camada de Segurança e Governança
- **RBAC (Role-Based Access Control):** Classifica cada ferramenta em `somente_leitura`, `operacional` ou `administrativo`.
- **Two-Phase Approval (HMAC-SHA256):** Ações de exclusão exigem geração de token criptográfico com TTL de 15 minutos, impedindo que agentes executem deleções acidentais.
- **Auditoria Local:** Registra todas as ações executadas em `audit_grafana_mcp.jsonl` com timestamp ISO 8601, parâmetros e tempo de execução em milissegundos.
- **Redação Automática de Credenciais:** Tokens, senhas e headers sensíveis são limpos antes de qualquer saída de log ou resposta.

### 3. Camada de Motores Especializados
- **Dashboard Builder:** Executa a orquestração em 9 fases para transformar prompts simples em dashboards prontos na API.
- **Query Validator:** Valida expressões PromQL, LogQL e aplica restrição estrita de leitura (`SELECT`/`WITH`) em fontes relacionais SQL.
- **Report Engine:** Renderiza relatórios corporativos multi-formato (PDF com tabelas e sumários, planilhas Excel XLSX e exportações estruturadas).

### 4. Camada de Transporte HTTP
- Utiliza `httpx.AsyncClient` com pool de conexões persistentes (*keep-alive*).
- Implementa controle de concorrência por semáforo assíncrono (`asyncio.Semaphore`).
- Mecanismo de retry automático com backoff exponencial para resiliência contra oscilações de rede.
