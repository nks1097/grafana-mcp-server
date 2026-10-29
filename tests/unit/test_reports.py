"""Testes dos exportadores de relatórios nos formatos PDF, XLSX, CSV e JSON."""

import os
import tempfile

from grafana_mcp.reports.exporters import (
    export_to_csv,
    export_to_json,
    export_to_markdown,
    export_to_pdf,
    export_to_xlsx,
)


def test_exportadores_arquivos():
    """Valida geração correta e integridade de arquivos de relatórios exportados."""
    with tempfile.TemporaryDirectory() as tmpdir:
        headers = ["Serviço", "Disponibilidade", "Status"]
        rows = [
            ["API Gateway", "99.99%", "OK"],
            ["Database Main", "99.95%", "OK"],
        ]

        # PDF
        pdf_path = os.path.join(tmpdir, "test.pdf")
        export_to_pdf("Relatório Teste", "Resumo de teste", headers, rows, pdf_path)
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 500

        # XLSX
        xlsx_path = os.path.join(tmpdir, "test.xlsx")
        export_to_xlsx("Planilha Teste", {"Métricas": {"headers": headers, "rows": rows}}, xlsx_path)
        assert os.path.exists(xlsx_path)
        assert os.path.getsize(xlsx_path) > 1000

        # CSV
        csv_path = os.path.join(tmpdir, "test.csv")
        export_to_csv(headers, rows, csv_path)
        assert os.path.exists(csv_path)
        with open(csv_path, encoding="utf-8") as f:
            content = f.read()
            assert "API Gateway" in content

        # JSON
        json_path = os.path.join(tmpdir, "test.json")
        export_to_json({"status": "ok", "rows": rows}, json_path)
        assert os.path.exists(json_path)

        # Markdown
        md_path = os.path.join(tmpdir, "test.md")
        export_to_markdown("Título MD", headers, rows, md_path)
        assert os.path.exists(md_path)
