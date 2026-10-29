# ⚙️ Referência de Configuração e Variáveis de Ambiente

O **Grafana MCP Server** utiliza uma camada centralizada de configurações baseada em Pydantic Settings, permitindo parametrização tanto via arquivo `.env` quanto diretamente por variáveis de ambiente do sistema operacional ou orquestrador (Docker / Kubernetes).

---

## 1. Tabela Completa de Variáveis de Ambiente

| Variável | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `GRAFANA_URL` | String | `http://192.168.0.107:3000` | URL base da API HTTP do Grafana (sem barra final). |
| `GRAFANA_API_TOKEN` | String | `None` | Token de Service Account (`glsa_...`) ou API Key legado (`ey...`). |
| `GRAFANA_USER` | String | `admin` | Usuário para autenticação básica alternativa. |
| `GRAFANA_PASSWORD` | String | `None` | Senha para autenticação básica alternativa. |
| `GRAFANA_ORG_ID` | Inteiro | `1` | ID numérico da organização do Grafana a operar. |
| `GRAFANA_TIMEOUT` | Float | `30.0` | Timeout máximo em segundos para requisições HTTP à API do Grafana. |
| `GRAFANA_VERIFY_TLS` | Booleano | `false` | Se deve validar certificados SSL/TLS em conexões HTTPS. |
| `GRAFANA_CA_BUNDLE` | String | `None` | Caminho do arquivo de certificados CA customizados. |
| `GRAFANA_MAX_RESULTS` | Inteiro | `100` | Limite padrão de paginação para buscas e listagens. |
| `GRAFANA_MAX_CONCURRENT_QUERIES` | Inteiro | `10` | Semáforo de concorrência máxima de requisições simultâneas. |
| `GRAFANA_DEFAULT_TIME_RANGE` | String | `now-6h` | Janela temporal padrão aplicada caso não seja informada. |
| `MCP_TRANSPORT` | String | `stdio` | Protocolo de transporte MCP (`stdio` para CLI local ou `sse` para HTTP). |
| `MCP_HOST` | String | `0.0.0.0` | Host de escuta quando executado em modo SSE. |
| `MCP_PORT` | Inteiro | `8001` | Porta TCP de escuta quando executado em modo SSE. |
| `MCP_MODE` | String | `operacional` | Nível de RBAC: `somente_leitura`, `operacional`, `administrativo`. |
| `MCP_READ_ONLY` | Booleano | `false` | Trava mestra que força modo estrito de leitura independente do `MCP_MODE`. |
| `MCP_REQUIRE_APPROVAL_DESTRUCTIVE` | Booleano | `true` | Exige token HMAC de dois passos para exclusão de dashboards, pastas e regras. |
| `MCP_APPROVAL_SECRET` | String | `chave-secreta...` | Segredo utilizado para assinar os tokens criptográficos HMAC-SHA256. |
| `MCP_AUDIT_ENABLED` | Booleano | `true` | Ativa a trilha de auditoria local em formato JSON Lines. |
| `MCP_AUDIT_PATH` | String | `./audit_grafana_mcp.jsonl` | Caminho do arquivo de log de auditoria. |
| `MCP_REPORT_OUTPUT_DIR` | String | `./reports_output` | Diretório de destino para exportação de PDFs e planilhas XLSX. |

---

## 2. Métodos de Autenticação Suportados

### 1. Service Account Token (Recomendado)
A partir do Grafana 9.1+, Service Accounts substituíram as chaves de API legadas.
Configure a variável:
```ini
GRAFANA_API_TOKEN=glsa_seu_token_de_servico_aqui_exemplo12345
```
O servidor enviará automaticamente o cabeçalho HTTP:
`Authorization: Bearer glsa_...`

### 2. Autenticação Básica (Usuário e Senha)
Caso o token não esteja configurado, o cliente utilizará automaticamente Basic Auth:
```ini
GRAFANA_USER=admin
GRAFANA_PASSWORD=Natanael1097
```

---

## 3. Modos de Operação (RBAC)

O servidor possui 3 níveis hierárquicos de permissão para garantir segurança em ambientes de produção:

1. **`somente_leitura` (Read-Only):**
   - Permite apenas consultas (`GET`), buscas, relatórios e diagnósticos.
   - Bloqueia qualquer criação, modificação ou exclusão de recursos.
2. **`operacional` (Operational - Padrão):**
   - Permite consultas e criação/edição de dashboards, painéis, anotações e regras de alerta.
   - Bloqueia operações administrativas de deleção permanente sem aprovação.
3. **`administrativo` (Administrative):**
   - Acesso irrestrito a governança de permissões, equipes, plugins e exclusões.
