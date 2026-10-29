"""Categoria F — Pastas, Organização e Navegação (Ferramentas 061 a 070)."""

import time
import urllib.parse
from typing import Any

from ..authorization import AuthorizationManager, PermissionLevel
from ..client import grafana_client
from ..config import settings
from ..models import ToolMetadata, ToolResult
from ..policies import ApprovalPolicyManager

auth_mgr = AuthorizationManager(settings.mcp_mode, settings.mcp_read_only)
policy_mgr = ApprovalPolicyManager(settings.mcp_approval_secret)


async def grafana_listar_pastas(limite: int = 100, pagina: int = 1) -> ToolResult:
    """61. Listar todas as pastas cadastradas no Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_pastas")
    t0 = time.time()
    try:
        folders = await grafana_client.request("GET", "/api/folders", params={"limit": limite, "page": pagina})
        clean = folders if isinstance(folders, list) else []
        return ToolResult(
            sucesso=True,
            dados={"pastas": clean, "total": len(clean)},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000, total_registros=len(clean)),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_criar_pasta(titulo: str, uid: str | None = None) -> ToolResult:
    """62. Criar uma nova pasta no Grafana com título e UID opcional."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_criar_pasta")
    t0 = time.time()
    try:
        payload = {"title": titulo}
        if uid:
            payload["uid"] = uid
        res = await grafana_client.request("POST", "/api/folders", json_data=payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_atualizar_pasta(uid: str, novo_titulo: str) -> ToolResult:
    """63. Atualizar o título ou propriedades de uma pasta existente."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_atualizar_pasta")
    t0 = time.time()
    try:
        payload = {"title": novo_titulo, "overwrite": True}
        res = await grafana_client.request("PUT", f"/api/folders/{uid}", json_data=payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_excluir_pasta(uid: str, token_aprovacao: str | None = None) -> ToolResult:
    """64. Excluir uma pasta e opcionalmente seus dashboards dependentes (Ação destrutiva - requer aprovação)."""
    auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_excluir_pasta")
    t0 = time.time()
    params = {"uid": uid}
    try:
        policy_mgr.verify_or_raise(
            token_aprovacao,
            "grafana_excluir_pasta",
            params,
            enabled=settings.mcp_require_approval_destructive,
        )
        res = await grafana_client.request("DELETE", f"/api/folders/{uid}")
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_mover_dashboard(uid_dashboard: str, nova_pasta_id: int) -> ToolResult:
    """65. Mover um dashboard existente para outra pasta no Grafana."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_mover_dashboard")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        payload = {
            "dashboard": dash,
            "folderId": nova_pasta_id,
            "overwrite": True,
            "message": f"Movido para pasta ID {nova_pasta_id} via MCP",
        }
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_listar_tags() -> ToolResult:
    """66. Listar todas as tags associadas a dashboards no Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_tags")
    t0 = time.time()
    try:
        tags = await grafana_client.request("GET", "/api/dashboards/tags")
        clean = tags if isinstance(tags, list) else []
        return ToolResult(
            sucesso=True,
            dados={"tags": clean, "total": len(clean)},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_pesquisar_recursos(
    consulta: str,
    tipo: str | None = None,  # "dash-db", "dash-folder"
    limite: int = 50,
) -> ToolResult:
    """67. Pesquisar recursos de forma ampla (dashboards, pastas e painéis) por palavra-chave."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_pesquisar_recursos")
    t0 = time.time()
    try:
        res = await grafana_client.search_resources(query=consulta, type_=tipo, limit=limite)
        return ToolResult(
            sucesso=True,
            dados={"resultados": res, "total": len(res)},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerar_link_explore(
    datasource_uid: str,
    consulta: str,
    de: str = "now-1h",
    ate: str = "now",
) -> ToolResult:
    """68. Gerar link navegável direto para o modo Explore com a consulta pré-carregada."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerar_link_explore")
    t0 = time.time()
    try:
        base = grafana_client.base_url
        import json

        panes = {
            "left": {
                "datasource": datasource_uid,
                "queries": [{"refId": "A", "expr": consulta, "query": consulta}],
                "range": {"from": de, "to": ate},
            }
        }
        encoded = urllib.parse.quote(json.dumps(panes))
        explore_url = f"{base}/explore?schemaVersion=1&panes={encoded}"
        return ToolResult(
            sucesso=True,
            dados={"url_explore": explore_url},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_snapshots(
    acao: str,  # "listar", "criar", "excluir"
    chave_snapshot: str | None = None,
    dashboard_dict: dict[str, Any] | None = None,
    nome: str | None = None,
) -> ToolResult:
    """69. Gerenciar snapshots estáticos e compartilháveis de dashboards."""
    t0 = time.time()
    try:
        if acao == "listar":
            auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerenciar_snapshots")
            res = await grafana_client.request("GET", "/api/dashboard/snapshots")
            return ToolResult(
                sucesso=True, dados={"snapshots": res}, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
            )

        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerenciar_snapshots")
        if acao == "criar" and dashboard_dict:
            payload = {"dashboard": dashboard_dict, "name": nome or "Snapshot MCP", "expires": 3600}
            res = await grafana_client.request("POST", "/api/snapshots", json_data=payload)
        elif acao == "excluir" and chave_snapshot:
            res = await grafana_client.request("DELETE", f"/api/snapshots/{chave_snapshot}")
        else:
            return ToolResult(sucesso=False, erro="Parâmetros ausentes para criação/exclusão de snapshot.")

        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_anotacoes(
    acao: str,  # "listar", "criar", "excluir"
    texto: str | None = None,
    tags: list[str] | None = None,
    id_anotacao: int | None = None,
    uid_dashboard: str | None = None,
) -> ToolResult:
    """70. Consultar, criar e excluir anotações em timelines de dashboards."""
    t0 = time.time()
    try:
        if acao == "listar":
            auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerenciar_anotacoes")
            params = {}
            if tags:
                params["tags"] = tags
            res = await grafana_client.request("GET", "/api/annotations", params=params)
            return ToolResult(
                sucesso=True, dados={"anotacoes": res}, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
            )

        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerenciar_anotacoes")
        if acao == "criar" and texto:
            payload = {
                "text": texto,
                "tags": tags or ["mcp", "deploy"],
                "time": int(time.time() * 1000),
            }
            res = await grafana_client.request("POST", "/api/annotations", json_data=payload)
        elif acao == "excluir" and id_anotacao:
            res = await grafana_client.request("DELETE", f"/api/annotations/{id_anotacao}")
        else:
            return ToolResult(sucesso=False, erro="Parâmetros ausentes para gerenciar anotações.")

        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
