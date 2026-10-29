# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.
O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/), e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-10-29

### Adicionado
- Servidor MCP universal para Grafana com 100 ferramentas em português.
- Criação e geração inteligente de dashboards por prompts em linguagem natural (9 estágios).
- Validação avançada de consultas PromQL, LogQL, SQL e Tempo.
- Motor corporativo de relatórios (PDF, Excel XLSX, CSV, JSON e Markdown).
- Suporte a RBAC (`somente_leitura`, `operacional`, `administrativo`).
- Sistema de aprovação em dois passos com tokens criptográficos HMAC-SHA256 para operações destrutivas.
- Redação automática de segredos em logs e respostas (tokens, senhas).
- Proteção contra SSRF e limites estritos de concorrência e timeout.
- Suporte aos transportes STDIO e SSE (Server-Sent Events).

