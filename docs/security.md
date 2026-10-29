# 🔒 Segurança, Governança e Auditoria

O **Grafana MCP Server** foi construído com foco em segurança defensiva e estrita aderência a padrões de governança para prevenir acidentes operacionais, vazamento de credenciais e violações de compliance em ambientes de produção.

---

## 1. Controle de Acesso Baseado em Funções (RBAC)

O servidor implementa 3 níveis hierárquicos de autorização:

```
[somente_leitura] (Nível 1)
       │
       ▼
 [operacional]    (Nível 2)
       │
       ▼
[administrativo]  (Nível 3)
```

- **`somente_leitura`:** Todas as chamadas que alteram estado (`POST`, `PUT`, `PATCH`, `DELETE`) são bloqueadas antes mesmo de tocar a rede. O agente só consegue ler métricas, listar dashboards e gerar relatórios.
- **`operacional` (Modo Recomendado):** Permite criação e ajuste de dashboards, testes de consulta e declaração de incidentes. Operações destrutivas como exclusão de dashboards ou pastas são interceptadas.
- **`administrativo`:** Habilita gerenciamento de equipes, permissões globais de pastas e exclusões controladas.

---

## 2. Confirmação em Dois Passos com Tokens HMAC-SHA256

Para eliminar o risco de um agente de IA deletar recursos importantes por engano ou alucinação, ferramentas destrutivas exigem aprovação explícita:

1. **Tentativa Inicial do Agente:**
   O agente chama `grafana_excluir_dashboard(uid="srv-linux-prod")` sem fornecer o token.
2. **Resposta do Servidor (Interrupção Preventiva):**
   A operação é bloqueada e o servidor gera um token HMAC com validade de 15 minutos:
   ```json
   {
     "sucesso": false,
     "erro": "Aprovação necessária para exclusão.",
     "dados": {
       "aprovacao_requerida": {
         "acao": "excluir_dashboard",
         "alvo": "srv-linux-prod",
         "token": "apr_1761748200_a9f1b4c3e8d7...",
         "validade_minutos": 15
       }
     }
   }
   ```
3. **Confirmação Explícita do Operador:**
   O operador valida e autoriza a execução reenviando o comando com o token:
   `grafana_excluir_dashboard(uid="srv-linux-prod", token_aprovacao="apr_1761748200_...")`
4. **Execução Segura:**
   O servidor valida a assinatura criptográfica e a data de expiração antes de executar a exclusão.

---

## 3. Restrição Estrita de Leitura em Consultas SQL

Fontes de dados relacionais (PostgreSQL, MySQL, ClickHouse, SQLite) conectadas ao Grafana possuem validação sintática prévia através do `QueryValidator`:
- Bloqueia comandos DDL: `DROP`, `CREATE`, `ALTER`, `TRUNCATE`.
- Bloqueia comandos DML modificadores: `DELETE`, `UPDATE`, `INSERT`.
- Bloqueia comandos de privilégios: `GRANT`, `REVOKE`.
- Aceita exclusivamente consultas iniciando com `SELECT` ou cláusulas `WITH`.

---

## 4. Redação Automática de Credenciais em Respostas e Logs

Qualquer cabeçalho HTTP ou campo contendo termos como `token`, `password`, `secret`, `glsa_`, `ey...` é automaticamente substituído por `[REDACTED]` antes de ser gravado em disco ou retornado ao modelo de linguagem.

---

## 5. Trilha de Auditoria Imutável (JSON Lines)

Todas as ações acionadas pelo servidor MCP são registradas em `audit_grafana_mcp.jsonl`:
```json
{
  "timestamp": "2026-10-29T10:10:13.120Z",
  "ferramenta": "grafana_salvar_dashboard",
  "sucesso": true,
  "duracao_ms": 112.5,
  "usuario": "mcp-agent",
  "parametros_sanitizados": {"uid": "linux-mon", "title": "Linux Monitoring"}
}
```
Isso permite fácil auditoria externa por times de compliance e SOC.

