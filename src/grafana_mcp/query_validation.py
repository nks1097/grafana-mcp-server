"""Validação e sanitização de consultas PromQL, LogQL, SQL e Tempo."""

import re
from typing import Any

from .exceptions import GrafanaValidationError


class QueryValidator:
    """Valida sintaxe básica, limites e segurança de consultas antes de executar."""

    DESTRUCTIVE_SQL_KEYWORDS = [
        r"\bDROP\b",
        r"\bDELETE\b",
        r"\bTRUNCATE\b",
        r"\bALTER\b",
        r"\bUPDATE\b",
        r"\bINSERT\b",
        r"\bCREATE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
    ]

    @classmethod
    def validate_promql(cls, query: str) -> dict[str, Any]:
        """Valida se a consulta PromQL é plausível."""
        q = query.strip()
        if not q:
            raise GrafanaValidationError("A consulta PromQL não pode ser vazia.")

        # Checagem básica de parênteses balanceados
        if q.count("(") != q.count(")"):
            raise GrafanaValidationError("Parênteses desbalanceados na consulta PromQL.")
        if q.count("{") != q.count("}"):
            raise GrafanaValidationError("Chaves de seletores desbalanceadas na consulta PromQL.")
        if q.count("[") != q.count("]"):
            raise GrafanaValidationError("Colchetes de intervalo temporal desbalanceados na consulta PromQL.")

        return {"valid": True, "type": "promql", "query": q}

    @classmethod
    def validate_logql(cls, query: str) -> dict[str, Any]:
        """Valida se a consulta LogQL possui seletor de streams válido."""
        q = query.strip()
        if not q:
            raise GrafanaValidationError("A consulta LogQL não pode ser vazia.")

        if not q.startswith("{") or "}" not in q:
            raise GrafanaValidationError(
                "A consulta LogQL deve iniciar com um seletor de stream entre chaves (ex: '{app=\"nginx\"}')."
            )

        return {"valid": True, "type": "logql", "query": q}

    @classmethod
    def validate_sql(cls, query: str) -> dict[str, Any]:
        """Valida que a consulta SQL é estritamente de leitura (SELECT)."""
        q = query.strip()
        if not q:
            raise GrafanaValidationError("A consulta SQL não pode ser vazia.")

        # Bloquear palavras-chave destrutivas
        for pattern in cls.DESTRUCTIVE_SQL_KEYWORDS:
            if re.search(pattern, q, re.IGNORECASE):
                raise GrafanaValidationError(
                    f"Consulta SQL rejeitada por conter comando modificador/destrutivo: {pattern}"
                )

        if not re.match(r"^(SELECT|WITH)\b", q, re.IGNORECASE):
            raise GrafanaValidationError("Consultas SQL no MCP Grafana devem iniciar com SELECT ou WITH.")

        return {"valid": True, "type": "sql", "query": q}

    @classmethod
    def validate_tempo(cls, query: str) -> dict[str, Any]:
        """Valida consulta TraceQL ou Trace ID."""
        q = query.strip()
        if not q:
            raise GrafanaValidationError("A consulta de trace não pode ser vazia.")

        return {"valid": True, "type": "tempo", "query": q}
