# Política de Segurança

A segurança é prioridade máxima no **Grafana MCP Server**.

## Relato de Vulnerabilidades

Caso encontre uma vulnerabilidade de segurança, solicitamos que **NÃO** abra uma issue pública.

Envie um e-mail detalhado para:
`natanael1097@gmail.com`

Inclua:
- Descrição da vulnerabilidade.
- Passos para reprodução ou Prova de Conceito (PoC).
- Versões afetadas do servidor MCP e do Grafana.
- Impacto potencial identificado.

Responderemos em até 48 horas úteis com o plano de mitigação.

## Boas Práticas Implementadas

- **RBAC Estrito:** O modo padrão é `somente_leitura`, impedindo modificações não autorizadas.
- **Aprovação HMAC em 2 Passos:** Operações destrutivas exigem token de aprovação assinado.
- **Redação Automática:** Segredos (Bearer tokens, senhas, chaves privadas) são mascarados antes de qualquer log ou retorno.
- **Proteção contra SSRF:** URLs arbitrárias são bloqueadas, restringindo o cliente exclusivamente ao host configurado em `GRAFANA_URL`.
