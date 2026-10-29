"""Testes de validação estática de consultas PromQL, LogQL e restrição SQL read-only."""

import pytest

from grafana_mcp.exceptions import GrafanaValidationError
from grafana_mcp.query_validation import QueryValidator


def test_promql_validation():
    """Valida sintaxe de consultas PromQL válidas e inválidas."""
    res_valida = QueryValidator.validate_promql('rate(node_cpu_seconds_total{mode="idle"}[5m])')
    assert res_valida["valid"] is True

    with pytest.raises(GrafanaValidationError):
        QueryValidator.validate_promql('rate(node_cpu_seconds_total{mode="idle"')


def test_logql_validation():
    """Valida sintaxe e presença de seletor de fluxo em consultas LogQL."""
    res_valida = QueryValidator.validate_logql('{app="nginx", env="prod"} |= "error"')
    assert res_valida["valid"] is True

    with pytest.raises(GrafanaValidationError):
        QueryValidator.validate_logql('|= "error"')


def test_sql_readonly_enforcement():
    """Garante bloqueio absoluto de comandos DDL/DML destrutivos em fontes SQL."""
    # Consultas SELECT válidas
    res_select = QueryValidator.validate_sql("SELECT id, name, count(*) FROM metrics GROUP BY id, name")
    assert res_select["valid"] is True

    # Bloqueio de DROP TABLE
    with pytest.raises(GrafanaValidationError):
        QueryValidator.validate_sql("DROP TABLE users;")

    # Bloqueio de UPDATE
    with pytest.raises(GrafanaValidationError):
        QueryValidator.validate_sql("UPDATE config SET val = 1;")

    # Bloqueio de DELETE
    with pytest.raises(GrafanaValidationError):
        QueryValidator.validate_sql("DELETE FROM audit_logs WHERE 1=1;")


def test_traceql_validation():
    """Valida filtros básicos de Trace."""
    res_valida = QueryValidator.validate_tempo("{ duration > 500ms }")
    assert res_valida["valid"] is True
