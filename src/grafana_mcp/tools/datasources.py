"""Categoria B — Fontes de Dados e Plugins (Ferramentas 021 a 030)."""

import time
from typing import Any

from ..authorization import AuthorizationManager, PermissionLevel
from ..client import grafana_client
from ..config import settings
from ..models import ToolMetadata, ToolResult
from ..policies import ApprovalPolicyManager

auth_mgr = AuthorizationManager(settings.mcp_mode, settings.mcp_read_only)
policy_mgr = ApprovalPolicyManager(settings.mcp_approval_secret)


async def grafana_listar_fontes_dados() -> ToolResult:
    """21. Listar todas as fontes de dados (datasources) configuradas no Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_fontes_dados")
    t0 = time.time()
    try:
        ds = await grafana_client.get_datasources()
        clean = [
            {
                "id": d.get("id"),
                "uid": d.get("uid"),
                "name": d.get("name"),
                "type": d.get("type"),
                "url": d.get("url"),
                "isDefault": d.get("isDefault"),
                "readOnly": d.get("readOnly"),
            }
            for d in ds
        ]
        return ToolResult(
            sucesso=True,
            dados={"fontes_dados": clean, "total": len(clean)},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000, total_registros=len(clean)),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_obter_fonte_dados(uid_ou_id: str) -> ToolResult:
    """22. Consultar detalhes e configurações não-sensíveis de uma fonte de dados específica."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_obter_fonte_dados")
    t0 = time.time()
    try:
        res = await grafana_client.request("GET", f"/api/datasources/uid/{uid_ou_id}")
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_criar_fonte_dados(
    nome: str,
    tipo: str,
    url: str,
    acesso: str = "proxy",
    padrao: bool = False,
    dados_adicionais: dict[str, Any] | None = None,
) -> ToolResult:
    """23. Criar uma nova fonte de dados no Grafana com parâmetros validados."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_criar_fonte_dados")
    t0 = time.time()
    try:
        payload = {
            "name": nome,
            "type": tipo,
            "url": url,
            "access": acesso,
            "isDefault": padrao,
            "jsonData": dados_adicionais or {},
        }
        res = await grafana_client.request("POST", "/api/datasources", json_data=payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_atualizar_fonte_dados(
    uid: str,
    nome: str | None = None,
    url: str | None = None,
    padrao: bool | None = None,
    dados_adicionais: dict[str, Any] | None = None,
) -> ToolResult:
    """24. Atualizar propriedades e configurações permitidas de uma fonte de dados existente."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_atualizar_fonte_dados")
    t0 = time.time()
    try:
        current = await grafana_client.request("GET", f"/api/datasources/uid/{uid}")
        if nome:
            current["name"] = nome
        if url:
            current["url"] = url
        if padrao is not None:
            current["isDefault"] = padrao
        if dados_adicionais:
            current.setdefault("jsonData", {}).update(dados_adicionais)

        ds_id = current.get("id")
        res = await grafana_client.request("PUT", f"/api/datasources/{ds_id}", json_data=current)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_excluir_fonte_dados(uid: str, token_aprovacao: str | None = None) -> ToolResult:
    """25. Excluir uma fonte de dados (Ação destrutiva - requer aprovação em dois passos)."""
    auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_excluir_fonte_dados")
    t0 = time.time()
    params = {"uid": uid}
    try:
        policy_mgr.verify_or_raise(
            token_aprovacao,
            "grafana_excluir_fonte_dados",
            params,
            enabled=settings.mcp_require_approval_destructive,
        )
        res = await grafana_client.request("DELETE", f"/api/datasources/uid/{uid}")
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_testar_fonte_dados(uid_ou_id: str) -> ToolResult:
    """26. Verificar conectividade e integridade de saúde de uma fonte de dados."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_testar_fonte_dados")
    t0 = time.time()
    try:
        res = await grafana_client.request("GET", f"/api/datasources/uid/{uid_ou_id}/health")
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_diagnosticar_fontes_dados() -> ToolResult:
    """27. Diagnosticar a saúde e conectividade de todas as fontes de dados cadastradas."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_diagnosticar_fontes_dados")
    t0 = time.time()
    try:
        ds_list = await grafana_client.get_datasources()
        diagnosticos = []
        for d in ds_list:
            uid = d.get("uid")
            name = d.get("name")
            tipo = d.get("type")
            status = "desconhecido"
            mensagem = ""
            try:
                h = await grafana_client.request("GET", f"/api/datasources/uid/{uid}/health")
                status = h.get("status", "OK")
                mensagem = h.get("message", "Conexão estabelecida com sucesso.")
            except Exception as ex:
                status = "ERRO"
                mensagem = str(ex)

            diagnosticos.append(
                {
                    "uid": uid,
                    "nome": name,
                    "tipo": tipo,
                    "status": status,
                    "mensagem": mensagem,
                }
            )

        return ToolResult(
            sucesso=True,
            dados={"fontes_avaliadas": len(diagnosticos), "diagnosticos": diagnosticos},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_listar_plugins() -> ToolResult:
    """28. Listar plugins instalados no Grafana (datasources, apps, painéis)."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_plugins")
    t0 = time.time()
    try:
        plugins = await grafana_client.request("GET", "/api/plugins")
        clean = [
            {
                "id": p.get("id"),
                "name": p.get("name"),
                "type": p.get("type"),
                "version": p.get("info", {}).get("version"),
                "enabled": p.get("enabled", True),
            }
            for p in (plugins if isinstance(plugins, list) else [])
        ]
        return ToolResult(
            sucesso=True,
            dados={"plugins": clean, "total": len(clean)},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_verificar_compatibilidade_plugin(plugin_id: str) -> ToolResult:
    """29. Verificar metadados e requisitos de compatibilidade de um plugin específico."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_verificar_compatibilidade_plugin")
    t0 = time.time()
    try:
        plugin = await grafana_client.request("GET", f"/api/plugins/{plugin_id}/settings")
        return ToolResult(sucesso=True, dados=plugin, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_listar_fontes_por_tipo(tipo: str) -> ToolResult:
    """30. Filtrar fontes de dados por tecnologia (ex: prometheus, loki, tempo, zabbix, postgres)."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_fontes_por_tipo")
    t0 = time.time()
    try:
        ds_list = await grafana_client.get_datasources()
        filtered = [d for d in ds_list if tipo.lower() in str(d.get("type", "")).lower()]
        return ToolResult(
            sucesso=True,
            dados={"tipo_filtrado": tipo, "fontes": filtered, "total": len(filtered)},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
