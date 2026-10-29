# 📊 Grafana MCP Server — 100 Tools in Portuguese for AI Agents

[![CI Pipeline](https://github.com/nks1097/grafana-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/nks1097/grafana-mcp-server/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![MCP Specification](https://img.shields.io/badge/MCP-2.3.0-green.svg)](https://modelcontextprotocol.io/)
[![Grafana Compatibility](https://img.shields.io/badge/Grafana-v9%20%7C%20v10%20%7C%20v11%20%7C%20v12%20%7C%20v13-orange.svg)](https://grafana.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-ready **Model Context Protocol (MCP)** server for autonomous Grafana management, AI-driven observability, automated dashboard provisioning, query optimization, and enterprise reporting. Features **100 functional tools in Portuguese**, tailored for SRE, DevOps, NOC, and SOC teams worldwide.

---

## 🌟 Key Features

- 🤖 **Prompt-to-Dashboard Engine (9 Stages):** Generates production-ready Grafana dashboards from natural language prompts, with automated grid positioning, panel planning, query synthesis, and API publishing.
- 🔍 **Static Query Validation:** Pre-validates PromQL, LogQL, TraceQL, and enforces strict read-only execution (`SELECT`/`WITH`) on SQL datasources.
- 📑 **Multi-Format Enterprise Reports:** Generates executive availability (SLA/SLO), performance, and capacity reports in **PDF (via ReportLab)**, **Excel (.xlsx via OpenPyXL)**, CSV, and JSON.
- 🛡️ **Defensive Governance & RBAC:** Features 3 operational modes (`somente_leitura`, `operacional`, `administrativo`), two-phase cryptographic **HMAC-SHA256** approval tokens for destructive operations, and automatic credential masking.
- 🌐 **Full Grafana Compatibility:** Validated against **Grafana v13.0.2**, with full backward support for v9.x, v10.x, v11.x, and v12.x (OSS, Enterprise, and Grafana Cloud).
- ⚡ **Dual Transport Modes:** Native support for **STDIO** (for local IDEs like Claude Desktop, Cursor, Antigravity IDE) and **SSE (Server-Sent Events)** for network and Docker deployments.

---

## 🚀 Quickstart Installation Guide

### 1. Requirements
- Python 3.11 or newer.
- An accessible Grafana instance (local, remote server, or Grafana Cloud).

### 2. Local Installation
```bash
git clone https://github.com/nks1097/grafana-mcp-server.git
cd grafana-mcp-server

python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -e .
```

### 3. Environment Configuration (`.env`)
```bash
cp .env.example .env
```

Set your instance URL and Service Account Token:
```ini
GRAFANA_URL=http://192.168.0.107:3000
GRAFANA_API_TOKEN=glsa_seu_token_de_servico_aqui_exemplo12345
MCP_MODE=operacional
```

---

## 💻 Client Integration (Claude Desktop, Cursor, Antigravity)

### Claude Desktop Configuration
In `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "grafana-mcp": {
      "command": "C:\\Users\\Natanael Krindges\\.gemini\\antigravity-ide\\mcp\\grafana\\.venv\\Scripts\\python.exe",
      "args": ["-m", "grafana_mcp.server", "--transport", "stdio"],
      "env": {
        "GRAFANA_URL": "http://192.168.0.107:3000",
        "GRAFANA_API_TOKEN": "glsa_seu_token_de_servico_aqui_exemplo12345",
        "MCP_MODE": "operacional"
      }
    }
  }
}
```

---

## 📋 The 100 Tools Overview

The server exports 100 dedicated tools across 9 core categories:
1. **Dashboards & Panels (`001-020`):** Automated creation, updates, duplication, grid positioning, variables, and validations.
2. **Datasources & Plugins (`021-030`):** Discovery, health checks, connectivity tests, and plugin management.
3. **Queries & Metrics (`031-040`):** PromQL, LogQL, Tempo, InfluxDB, and SQL query execution and statistical anomaly detection.
4. **Logs, Traces & Observability (`041-050`):** Error pattern discovery, slow span inspection, full trace trees, and 360° telemetry correlation.
5. **Alerting & Notifications (`051-060`):** Unified Alerting rules, contact points, silences, and flapping diagnostic.
6. **Folders, Tags & Annotations (`061-070`):** Resource organization, snapshots, and timeline event annotations.
7. **Reports & Rendering (`071-080`):** PDF and Excel report generation for SLA, capacity planning, and PNG panel rendering.
8. **Incidents, SLOs & OnCall (`081-090`):** Incident lifecycle management, on-call schedules, error budget burn rates, and post-mortem generation.
9. **Administration & Governance (`091-100`):** Health check, users, teams, permissions ACL, security audit, and connectivity tests.

For detailed documentation on each tool, refer to [docs/tools-reference.md](docs/tools-reference.md).

---

## 🧪 Testing

Run unit and integration test suites:
```bash
pytest tests -v
```

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
