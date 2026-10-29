"""Testes do sistema de autorização RBAC e políticas de aprovação HMAC."""

import pytest

from grafana_mcp.authorization import AuthorizationManager, PermissionLevel
from grafana_mcp.exceptions import GrafanaPermissionError
from grafana_mcp.policies import ApprovalPolicyManager


def test_rbac_somente_leitura():
    """Valida bloqueio de operações operacionais e administrativas no modo somente_leitura."""
    auth_mgr = AuthorizationManager(current_mode="somente_leitura", read_only_override=True)

    # Leitura é permitida
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_dashboards")

    # Escrita operacional é bloqueada
    with pytest.raises(GrafanaPermissionError):
        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_criar_dashboard")

    # Escrita administrativa é bloqueada
    with pytest.raises(GrafanaPermissionError):
        auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_excluir_dashboard")


def test_rbac_modo_operacional():
    """Valida permissões no modo operacional."""
    auth_mgr = AuthorizationManager(current_mode="operacional", read_only_override=False)

    # Leitura permitida
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_fontes_dados")
    # Operacional permitida
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_criar_dashboard")

    # Administrativa é bloqueada
    with pytest.raises(GrafanaPermissionError):
        auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_excluir_fonte_dados")


def test_hmac_approval_flow():
    """Valida ciclo completo de geração e validação de token de aprovação HMAC."""
    policy_mgr = ApprovalPolicyManager(secret="segredo-teste-unitario")

    req = policy_mgr.generate_approval_request(
        action="excluir_dashboard",
        target="uid-dash-123",
        description="Exclusão de teste de dashboard",
    )

    assert "token" in req
    token = req["token"]

    # Token correto e dentro do prazo é aprovado
    assert policy_mgr.verify_approval(token, "excluir_dashboard", "uid-dash-123") is True

    # Token para outra ação é rejeitado
    assert policy_mgr.verify_approval(token, "outra_acao", "uid-dash-123") is False

    # Token para outro alvo é rejeitado
    assert policy_mgr.verify_approval(token, "excluir_dashboard", "outro-uid") is False

    # Token adulterado é rejeitado
    assert policy_mgr.verify_approval(token + "invalido", "excluir_dashboard", "uid-dash-123") is False
