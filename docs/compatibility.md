# 🧩 Matriz de Compatibilidade com o Grafana

O **Grafana MCP Server** foi desenvolvido para oferecer máxima compatibilidade retroativa e futura com a API HTTP oficial do Grafana.

---

## 1. Versões Suportadas do Grafana

| Versão do Grafana | Status | Observações |
| :--- | :--- | :--- |
| **Grafana 13.x** | ✅ Testado e Validado | Totalmente suportado (testado ativamente na versão v13.0.2). |
| **Grafana 12.x** | ✅ Suportado | Totalmente compatível com Unified Alerting e Provisioning APIs. |
| **Grafana 11.x** | ✅ Suportado | Suporte completo a Service Accounts e novo painel de visualizações. |
| **Grafana 10.x** | ✅ Suportado | Compatibilidade total com `schemaVersion` 36+. |
| **Grafana 9.x** | ⚠️ Suportado com Limitações | Requer Grafana 9.1+ para Service Accounts. |
| **Grafana 8.x ou anterior** | ❌ Não Recomendado | APIs de provisionamento e Alerting legado incompatíveis. |

---

## 2. Tipos de Distribuição

- **Grafana Open Source (OSS):** 100% suportado para todas as 100 ferramentas (com fallbacks inteligentes para plugins opcionais como Incident e SLO).
- **Grafana Enterprise:** 100% suportado, incluindo relatórios corporativos e recursos avançados de auditoria.
- **Grafana Cloud:** 100% suportado utilizando tokens de Service Account e endpoint HTTPS do stack (ex: `https://seu-slug.grafana.net`).

---

## 3. Fontes de Dados Suportadas para Consultas

- **Prometheus / Mimir / Thanos:** Consultas PromQL instantâneas e em intervalos.
- **Grafana Loki:** Consultas LogQL de streams e métricas.
- **Grafana Tempo:** Consultas TraceQL e busca de spans.
- **Alexander Zobnin Zabbix Datasource:** Totalmente integrado para métricas do agente Zabbix.
- **PostgreSQL / MySQL / ClickHouse:** Consultas SQL com validação read-only.
- **InfluxDB:** Consultas temporais Flux e InfluxQL.

