# 🚀 Guia Completo de Instalação e Configuração — Grafana MCP Server

Este guia fornece o passo a passo completo e detalhado para instalar, configurar e integrar o **Grafana MCP Server** em qualquer ambiente operacional e cliente MCP compatível.

---

## 1. Pré-requisitos

- **Python:** Versão 3.11, 3.12, 3.13 ou superior.
- **Grafana:** Instância Grafana v9.x, v10.x, v11.x, v12.x ou v13.x (OSS, Enterprise ou Grafana Cloud).
- **Acesso à API:** URL da instância (ex: `http://192.168.0.107:3000`) e um **Service Account Token** ou usuário/senha.

---

## 2. Como Gerar o Token no Grafana (Recomendado)

O método mais seguro e moderno para autenticar no Grafana é através de um **Service Account Token**:

1. No Grafana, acesse o menu lateral: **Administration** -> **Users and access** -> **Service accounts**.
2. Clique no botão **Add service account**.
3. Defina um nome (ex: `mcp-server-agent`) e atribua a função (*Role*):
   - `Viewer`: Para uso em modo `somente_leitura`.
   - `Editor`: Para criação e edição de dashboards e alertas.
   - `Admin`: Para administração total de pastas, permissões e fontes de dados.
4. Clique em **Create** e depois em **Add service account token**.
5. Copie o token gerado (inicia com `glsa_...`). Guarde-o com segurança, pois ele não será exibido novamente.

---

## 3. Instalação Local (Python Virtualenv)

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/nks1097/grafana-mcp-server.git
cd grafana-mcp-server
```

### Passo 2: Criar e Ativar o Ambiente Virtual
**No Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Passo 3: Instalar as Dependências
```bash
pip install --upgrade pip
pip install -e .
```

---

## 4. Configuração das Variáveis de Ambiente

Copie o arquivo de exemplo `.env.example` para `.env`:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```ini
# Endereço da instância do Grafana
GRAFANA_URL=http://192.168.0.107:3000

# Token de Service Account (Recomendado)
GRAFANA_API_TOKEN=glsa_seu_token_de_servico_aqui_exemplo12345

# Autenticação alternativa (Basic Auth - usada caso o token não seja informado)
GRAFANA_USER=admin
GRAFANA_PASSWORD=sua_senha_aqui

# Governança e Segurança
MCP_MODE=operacional             # Opções: somente_leitura, operacional, administrativo
MCP_READ_ONLY=false
MCP_REQUIRE_APPROVAL_DESTRUCTIVE=true
MCP_APPROVAL_SECRET=sua-chave-secreta-hmac-aqui

# Transporte e Auditoria
MCP_TRANSPORT=stdio              # Opções: stdio ou sse
MCP_AUDIT_ENABLED=true
MCP_AUDIT_PATH=./audit_grafana_mcp.jsonl
MCP_REPORT_OUTPUT_DIR=./reports_output
```

---

## 5. Configuração nos Clientes MCP

### A. Claude Desktop
Localize o arquivo de configuração do Claude Desktop:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Adicione a seção do servidor:
```json
{
  "mcpServers": {
    "grafana-mcp": {
      "command": "C:\\Users\\Natanael Krindges\\.gemini\\antigravity-ide\\mcp\\grafana\\.venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "grafana_mcp.server",
        "--transport",
        "stdio"
      ],
      "env": {
        "GRAFANA_URL": "http://192.168.0.107:3000",
        "GRAFANA_API_TOKEN": "glsa_seu_token_de_servico_aqui_exemplo12345",
        "MCP_MODE": "operacional"
      }
    }
  }
}
```

### B. Antigravity IDE / VS Code
No arquivo de configuração MCP (`mcp_config.json` ou `.vscode/settings.json`):
```json
{
  "mcpServers": {
    "grafana-mcp": {
      "command": "C:/Users/Natanael Krindges/.gemini/antigravity-ide/mcp/grafana/.venv/Scripts/python.exe",
      "args": ["-m", "grafana_mcp.server"],
      "env": {
        "GRAFANA_URL": "http://192.168.0.107:3000",
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
      "cwd": "C:\\Users\\Natanael Krindges\\.gemini\\antigravity-ide\\mcp\\grafana",
      "env": {
        "GRAFANA_URL": "http://192.168.0.107:3000",
        "GRAFANA_API_TOKEN": "glsa_seu_token_de_servico_aqui_exemplo12345"
      }
    }
  }
}
```

---

## 6. Execução via Docker e Docker Compose (Transporte SSE)

Se preferir rodar em contêiner com transporte Server-Sent Events (SSE) via rede:

```bash
docker compose up -d --build
```

O servidor estará escutando em `http://localhost:8001/sse`.

Para integrar com clientes HTTP SSE, utilize:
```json
{
  "mcpServers": {
    "grafana-mcp-sse": {
      "url": "http://localhost:8001/sse"
    }
  }
}
```

---

## 7. Como Testar e Validar a Instalação

Execute o comando de teste rápido para validar a conexão imediata com o seu Grafana:
```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from grafana_mcp.tools import grafana_testar_conexao; print(asyncio.run(grafana_testar_conexao()))"
```

Saída esperada:
```json
{
  "sucesso": true,
  "dados": {
    "status": "CONECTADO COM SUCESSO",
    "url_alvo": "http://192.168.0.107:3000",
    "versao_grafana": "13.0.2",
    "latencia_ms": 58.4,
    "autenticacao": "VÁLIDA (Token / Credencial Aceita)",
    "datasources_detectadas": 1
  }
}
```
