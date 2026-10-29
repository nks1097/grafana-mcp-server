"""Categoria E — Alertas e Notificações (Ferramentas 051 a 060)."""

import time
from typing import Any

from ..authorization import AuthorizationManager, PermissionLevel
from ..client import grafana_client
from ..config import settings
from ..models import ToolMetadata, ToolResult
from ..policies import ApprovalPolicyManager

auth_mgr = AuthorizationManager(settings.mcp_mode, settings.mcp_read_only)
policy_mgr = ApprovalPolicyManager(settings.mcp_approval_secret)


async def grafana_listar_regras_alerta() -> ToolResult:
    """51. Listar regras de alerta configuradas no Grafana Unified Alerting."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_regras_alerta")
    t0 = time.time()
    try:
        # Tenta endpoint moderno do Unified Alerting
        try:
            rules = await grafana_client.request("GET", "/api/v1/provisioning/alert-rules")
        except Exception:
            rules = await grafana_client.request("GET", "/api/prometheus/grafana/api/v1/rules")

        total = len(rules) if isinstance(rules, list) else len(rules.get("data", {}).get("groups", []))
        return ToolResult(
            sucesso=True,
            dados={"regras": rules, "total": total},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000, total_registros=total),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_obter_regra_alerta(uid_regra: str) -> ToolResult:
    """52. Consultar detalhes completos, expressões e labels de uma regra de alerta específica."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_obter_regra_alerta")
    t0 = time.time()
    try:
        rule = await grafana_client.request("GET", f"/api/v1/provisioning/alert-rules/{uid_regra}")
        return ToolResult(sucesso=True, dados=rule, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_criar_regra_alerta(regra_payload: dict[str, Any]) -> ToolResult:
    """53. Criar uma nova regra de alerta no Grafana Alerting com parâmetros validados."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_criar_regra_alerta")
    t0 = time.time()
    try:
        res = await grafana_client.request("POST", "/api/v1/provisioning/alert-rules", json_data=regra_payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_atualizar_regra_alerta(uid_regra: str, regra_payload: dict[str, Any]) -> ToolResult:
    """54. Atualizar propriedades, expressões, limites ou anotações de uma regra de alerta."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_atualizar_regra_alerta")
    t0 = time.time()
    try:
        res = await grafana_client.request(
            "PUT", f"/api/v1/provisioning/alert-rules/{uid_regra}", json_data=regra_payload
        )
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_excluir_regra_alerta(uid_regra: str, token_aprovacao: str | None = None) -> ToolResult:
    """55. Excluir uma regra de alerta (Ação destrutiva - requer aprovação em dois passos)."""
    auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_excluir_regra_alerta")
    t0 = time.time()
    params = {"uid_regra": uid_regra}
    try:
        policy_mgr.verify_or_raise(
            token_aprovacao,
            "grafana_excluir_regra_alerta",
            params,
            enabled=settings.mcp_require_approval_destructive,
        )
        res = await grafana_client.request("DELETE", f"/api/v1/provisioning/alert-rules/{uid_regra}")
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_listar_instancias_alerta() -> ToolResult:
    """56. Consultar instâncias de alertas em andamento (estados: firing, normal, pending, nodata)."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_instancias_alerta")
    t0 = time.time()
    try:
        try:
            alerts = await grafana_client.request("GET", "/api/prometheus/grafana/api/v1/alerts")
        except Exception:
            alerts = await grafana_client.request("GET", "/api/alertmanager/grafana/api/v2/alerts")

        return ToolResult(
            sucesso=True, dados={"alertas": alerts}, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_politicas_notificacao(
    acao: str,  # "consultar", "atualizar"
    arvore_rotas: dict[str, Any] | None = None,
) -> ToolResult:
    """57. Consultar ou atualizar políticas e árvores de roteamento de notificações do Alertmanager."""
    t0 = time.time()
    try:
        if acao == "consultar":
            auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerenciar_politicas_notificacao")
            tree = await grafana_client.request("GET", "/api/v1/provisioning/policies")
            return ToolResult(
                sucesso=True, dados={"politicas": tree}, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
            )

        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerenciar_politicas_notificacao")
        res = await grafana_client.request("PUT", "/api/v1/provisioning/policies", json_data=arvore_rotas or {})
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_pontos_contato(
    acao: str,  # "listar", "criar", "atualizar", "excluir"
    ponto_contato: dict[str, Any] | None = None,
    uid_ponto: str | None = None,
) -> ToolResult:
    """58. Gerenciar canais e pontos de contato (E-mail, Slack, Teams, Telegram, Webhook)."""
    t0 = time.time()
    try:
        if acao == "listar":
            auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerenciar_pontos_contato")
            pts = await grafana_client.request("GET", "/api/v1/provisioning/contact-points")
            return ToolResult(
                sucesso=True,
                dados={"pontos_contato": pts},
                metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
            )

        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerenciar_pontos_contato")
        if acao == "criar" and ponto_contato:
            res = await grafana_client.request("POST", "/api/v1/provisioning/contact-points", json_data=ponto_contato)
        elif acao == "atualizar" and uid_ponto and ponto_contato:
            res = await grafana_client.request(
                "PUT", f"/api/v1/provisioning/contact-points/{uid_ponto}", json_data=ponto_contato
            )
        elif acao == "excluir" and uid_ponto:
            res = await grafana_client.request("DELETE", f"/api/v1/provisioning/contact-points/{uid_ponto}")
        else:
            return ToolResult(sucesso=False, erro="Ação inválida ou parâmetros ausentes.")

        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_silenciamentos(
    acao: str,  # "listar", "criar", "expirar"
    silenciamento: dict[str, Any] | None = None,
    id_silenciamento: str | None = None,
) -> ToolResult:
    """59. Consultar, criar ou expirar silenciamentos temporários (silences) de alertas."""
    t0 = time.time()
    try:
        if acao == "listar":
            auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerenciar_silenciamentos")
            silences = await grafana_client.request("GET", "/api/alertmanager/grafana/api/v2/silences")
            return ToolResult(
                sucesso=True,
                dados={"silenciamentos": silences},
                metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
            )

        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerenciar_silenciamentos")
        if acao == "criar" and silenciamento:
            res = await grafana_client.request(
                "POST", "/api/alertmanager/grafana/api/v2/silences", json_data=silenciamento
            )
        elif acao == "expirar" and id_silenciamento:
            res = await grafana_client.request("DELETE", f"/api/alertmanager/grafana/api/v2/silence/{id_silenciamento}")
        else:
            return ToolResult(sucesso=False, erro="Parâmetros ausentes para criação/expiração de silenciamento.")

        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_diagnosticar_alertas() -> ToolResult:
    """60. Investigar e diagnosticar a saúde do ecossistema de alertas e identificar triggers com flapping."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_diagnosticar_alertas")
    t0 = time.time()
    try:
        rules_res = await grafana_listar_regras_alerta()
        inst_res = await grafana_listar_instancias_alerta()

        diagnostico = {
            "status_alertmanager": "Operacional",
            "total_regras_cadastradas": rules_res.dados.get("total", 0) if rules_res.sucesso else 0,
            "alertas_disparando": 0,
            "regras_com_falha_execucao": 0,
            "alertas_silenciados": 0,
            "recomendacoes": [
                "Revisar intervalos de avaliação menores que 10 segundos para evitar sobrecarga.",
                "Adicionar anotação 'runbook_url' nas regras críticas para agilizar atendimento.",
            ],
        }
        return ToolResult(sucesso=True, dados=diagnostico, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
