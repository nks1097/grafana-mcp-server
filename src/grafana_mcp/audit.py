"""Motor de auditoria local em JSON Lines (audit_grafana_mcp.jsonl)."""

import json
import os
import time
from typing import Any

from .auth import GrafanaAuth


class AuditLogger:
    """Registrador imutável de todas as invocações de ferramentas do MCP."""

    def __init__(self, log_path: str, enabled: bool = True) -> None:
        self.log_path = log_path
        self.enabled = enabled
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        if self.enabled:
            dirname = os.path.dirname(self.log_path)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)

    def log_call(
        self,
        tool_name: str,
        params: dict[str, Any],
        duration_ms: float,
        success: bool,
        error: str | None = None,
        auth_helper: GrafanaAuth | None = None,
    ) -> None:
        if not self.enabled:
            return

        record = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tool": tool_name,
            "params": params,
            "duration_ms": round(duration_ms, 2),
            "success": success,
            "error": error,
        }

        # Redação de segredos no registro
        raw_json = json.dumps(record, default=str)
        if auth_helper:
            raw_json = auth_helper.redact_secret(raw_json)

        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(raw_json + "\n")
        except Exception:
            pass  # Auditoria não deve quebrar a execução principal
