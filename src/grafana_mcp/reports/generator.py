"""Gerador profissional de relatórios corporativos para o Grafana MCP Server."""

import os
import time
from typing import Any

from .exporters import export_to_csv, export_to_json, export_to_markdown, export_to_pdf, export_to_xlsx


class ReportGenerator:
    """Consolida métricas e metadados e gera relatórios em múltiplos formatos."""

    def __init__(self, output_dir: str = "./reports_output") -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report(
        self,
        report_type: str,
        title: str,
        summary_text: str,
        headers: list[str],
        rows: list[list[Any]],
        format_type: str = "pdf",
    ) -> dict[str, Any]:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename_base = f"{report_type}_{timestamp}"

        if format_type.lower() == "pdf":
            filepath = os.path.join(self.output_dir, f"{filename_base}.pdf")
            export_to_pdf(title, summary_text, headers, rows, filepath)
        elif format_type.lower() in ("xlsx", "excel"):
            filepath = os.path.join(self.output_dir, f"{filename_base}.xlsx")
            sheets = {"Dados Consolidados": {"headers": headers, "rows": rows}}
            export_to_xlsx(title, sheets, filepath)
        elif format_type.lower() == "csv":
            filepath = os.path.join(self.output_dir, f"{filename_base}.csv")
            export_to_csv(headers, rows, filepath)
        elif format_type.lower() == "json":
            filepath = os.path.join(self.output_dir, f"{filename_base}.json")
            data = {"title": title, "summary": summary_text, "headers": headers, "rows": rows}
            export_to_json(data, filepath)
        else:
            filepath = os.path.join(self.output_dir, f"{filename_base}.md")
            export_to_markdown(title, headers, rows, filepath)

        return {
            "tipo_relatorio": report_type,
            "titulo": title,
            "formato": format_type.lower(),
            "caminho_arquivo": filepath,
            "total_linhas": len(rows),
            "timestamp": timestamp,
        }
