# 🛠️ Solução de Problemas (Troubleshooting)

Este documento reúne os erros mais frequentes encontrados durante a integração do **Grafana MCP Server** e o passo a passo para solucioná-los rapidamente.

---

## 1. Conexão Recusada (`Connection Refused` / `WinError 10061`)

### Sintoma
```text
Erro: Não foi possível conectar ao Grafana em 'http://localhost:3000': [WinError 10061] Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente.
```

### Causa
O Grafana não está escutando na interface de loopback (`localhost` / `127.0.0.1`) ou está rodando em outro IP da rede local (LAN).

### Solução
1. Verifique em qual IP e porta o Grafana está escutando. Se estiver na rede local (ex: `192.168.0.107:3000`), edite o arquivo `.env`:
   ```ini
   GRAFANA_URL=http://192.168.0.107:3000
   ```
2. Teste o endpoint de saúde no navegador ou via curl:
   ```bash
   curl http://192.168.0.107:3000/api/health
   ```
   Deve responder: `{"commit":"...","database":"ok","version":"13.0.2"}`.

---

## 2. Erro 401 Unauthorized / Token Inválido

### Sintoma
```text
Erro: Falha na autenticação com o Grafana (HTTP 401). Verifique o token de API ou usuário/senha.
```

### Causa
- O token fornecido expirou ou foi excluído no Grafana.
- O token foi copiado com espaços em branco ou aspas extras.

### Solução
1. No Grafana, acesse: **Administration** -> **Users and access** -> **Service accounts**.
2. Gere um novo token e cole exatamente o valor no `.env`:
   ```ini
   GRAFANA_API_TOKEN=glsa_seu_token_de_servico_aqui_exemplo12345
   ```

---

## 3. Erro 403 Forbidden / Permissão Insuficiente

### Sintoma
```text
Erro: O usuário não possui permissão para salvar dashboards (HTTP 403).
```

### Causa
A Service Account foi criada com a função `Viewer`, que não possui permissão de escrita.

### Solução
Altere a função da Service Account no Grafana para `Editor` ou `Admin`.

---

## 4. O Servidor MCP não Aparece no Claude Desktop ou Antigravity IDE

### Sintoma
O cliente de IA não lista as ferramentas com prefixo `grafana_`.

### Causa
O caminho do executável do Python ou os argumentos no arquivo de configuração do cliente MCP estão incorretos.

### Solução
1. No Windows, utilize barras invertidas duplas (`\\`) ou barras normais (`/`) no JSON:
   ```json
   "command": "C:/Users/Natanael Krindges/.gemini/antigravity-ide/mcp/grafana/.venv/Scripts/python.exe",
   "args": ["-m", "grafana_mcp.server"]
   ```
2. Certifique-se de que o ambiente virtual possui o pacote instalado:
   ```bash
   pip install -e .
   ```
3. Verifique os logs de inicialização do cliente MCP para confirmar que não houve erro de sintaxe no JSON.

---

## 5. Falha na Renderização de Imagens PNG (`grafana_renderizar_painel`)

### Sintoma
A ferramenta retorna a URL de renderização, mas ao abrir o link ocorre erro 404 ou 500.

### Causa
O Grafana requer o plugin oficial `grafana-image-renderer` instalado no servidor para converter painéis em imagens estáticas PNG.

### Solução
Instale o plugin na sua instância Grafana:
```bash
grafana-cli plugins install grafana-image-renderer
# Reinicie o serviço do Grafana
sudo systemctl restart grafana-server
```
