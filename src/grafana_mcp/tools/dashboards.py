"""Categoria A — Dashboards e Painéis (Ferramentas 001 a 020)."""

import time
import uuid
from typing import Any

from ..authorization import AuthorizationManager, PermissionLevel
from ..client import grafana_client
from ..config import settings
from ..dashboard_builder import DashboardBuilder
from ..dashboard_validator import DashboardValidator
from ..models import ToolMetadata, ToolResult
from ..policies import ApprovalPolicyManager

auth_mgr = AuthorizationManager(settings.mcp_mode, settings.mcp_read_only)
policy_mgr = ApprovalPolicyManager(settings.mcp_approval_secret)


async def grafana_listar_dashboards(
    consulta: str | None = None,
    tag: str | None = None,
    pasta_ids: list[int] | None = None,
    limite: int = 100,
    pagina: int = 1,
) -> ToolResult:
    """1. Pesquisar e listar dashboards cadastrados no Grafana com filtros por nome, tag e pasta."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_dashboards")
    t0 = time.time()
    try:
        raw = await grafana_client.search_resources(
            query=consulta,
            tag=tag,
            type_="dash-db",
            folder_ids=pasta_ids,
            limit=limite,
            page=pagina,
        )
        return ToolResult(
            sucesso=True,
            dados={"dashboards": raw, "total": len(raw)},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000, total_registros=len(raw)),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_obter_dashboard(uid: str) -> ToolResult:
    """2. Recuperar a definição JSON completa de um dashboard pelo seu UID."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_obter_dashboard")
    t0 = time.time()
    try:
        data = await grafana_client.get_dashboard(uid)
        return ToolResult(
            sucesso=True,
            dados=data,
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_obter_resumo_dashboard(uid: str) -> ToolResult:
    """3. Recuperar metadados e lista resumida de painéis sem retornar JSON excessivo."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_obter_resumo_dashboard")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        panels_summary = [
            {"id": p.get("id"), "title": p.get("title"), "type": p.get("type")} for p in dash.get("panels", [])
        ]
        resumo = {
            "uid": dash.get("uid"),
            "titulo": dash.get("title"),
            "tags": dash.get("tags", []),
            "versao": dash.get("version"),
            "total_paineis": len(panels_summary),
            "paineis": panels_summary,
            "pasta": meta.get("folderTitle"),
            "url": meta.get("url"),
        }
        return ToolResult(sucesso=True, dados=resumo, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_obter_painel(uid_dashboard: str, id_painel: int) -> ToolResult:
    """4. Recuperar a configuração e consultas de um painel específico de um dashboard."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_obter_painel")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        target_panel = None
        for p in dash.get("panels", []):
            if p.get("id") == id_painel:
                target_panel = p
                break
        if not target_panel:
            return ToolResult(
                sucesso=False,
                erro=f"Painel com ID {id_painel} não foi encontrado no dashboard {uid_dashboard}.",
                metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
            )
        return ToolResult(
            sucesso=True, dados=target_panel, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_criar_dashboard(
    dashboard: dict[str, Any],
    pasta_id: int = 0,
    pasta_uid: str | None = None,
    sobrescrever: bool = False,
    mensagem_commit: str | None = None,
) -> ToolResult:
    """5. Criar um novo dashboard validado no Grafana."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_criar_dashboard")
    t0 = time.time()
    try:
        payload = {
            "dashboard": dashboard,
            "folderId": pasta_id,
            "folderUid": pasta_uid,
            "overwrite": sobrescrever,
            "message": mensagem_commit or "Criado via Grafana MCP Server",
        }
        DashboardValidator.validate_dashboard_dict(payload)
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_atualizar_dashboard(
    dashboard: dict[str, Any],
    pasta_id: int | None = None,
    pasta_uid: str | None = None,
    mensagem_commit: str | None = None,
) -> ToolResult:
    """6. Atualizar a definição de um dashboard existente."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_atualizar_dashboard")
    t0 = time.time()
    try:
        payload = {
            "dashboard": dashboard,
            "folderId": pasta_id if pasta_id is not None else 0,
            "folderUid": pasta_uid,
            "overwrite": True,
            "message": mensagem_commit or "Atualizado via Grafana MCP Server",
        }
        DashboardValidator.validate_dashboard_dict(payload)
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_excluir_dashboard(uid: str, token_aprovacao: str | None = None) -> ToolResult:
    """7. Excluir um dashboard pelo UID (Ação destrutiva - requer aprovação em dois passos)."""
    auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_excluir_dashboard")
    t0 = time.time()
    params = {"uid": uid}
    try:
        policy_mgr.verify_or_raise(
            token_aprovacao,
            "grafana_excluir_dashboard",
            params,
            enabled=settings.mcp_require_approval_destructive,
        )
        res = await grafana_client.delete_dashboard(uid)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_duplicar_dashboard(
    uid_origem: str,
    novo_titulo: str,
    nova_pasta_id: int = 0,
) -> ToolResult:
    """8. Duplicar um dashboard existente com um novo título e UID."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_duplicar_dashboard")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_origem)
        dash = raw.get("dashboard", {})
        dash["id"] = None
        dash["uid"] = f"copy-{uuid.uuid4().hex[:10]}"
        dash["title"] = novo_titulo
        dash["version"] = 0

        payload = {
            "dashboard": dash,
            "folderId": nova_pasta_id,
            "overwrite": False,
            "message": f"Clonado a partir do dashboard {uid_origem}",
        }
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_variaveis_dashboard(
    uid_dashboard: str,
    acao: str,  # "listar", "adicionar", "remover"
    variavel: dict[str, Any] | None = None,
    nome_variavel: str | None = None,
) -> ToolResult:
    """9. Gerenciar variáveis de templating (filtros dinâmicos) de um dashboard."""
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        templating = dash.get("templating", {})
        var_list = templating.get("list", [])

        if acao == "listar":
            return ToolResult(
                sucesso=True,
                dados={"variaveis": var_list},
                metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
            )

        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerenciar_variaveis_dashboard")
        if acao == "adicionar" and variavel:
            var_list.append(variavel)
        elif acao == "remover" and nome_variavel:
            var_list = [v for v in var_list if v.get("name") != nome_variavel]

        templating["list"] = var_list
        dash["templating"] = templating

        payload = {
            "dashboard": dash,
            "folderId": meta.get("folderId", 0),
            "overwrite": True,
            "message": f"Variáveis alteradas ({acao}) via MCP",
        }
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerar_link_dashboard(
    uid: str,
    id_painel: int | None = None,
    intervalo_tempo: str | None = None,
    variaveis: dict[str, str] | None = None,
) -> ToolResult:
    """10. Gerar links e URLs navegáveis válidas para dashboards e painéis específicos."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_gerar_link_dashboard")
    t0 = time.time()
    try:
        base = grafana_client.base_url
        link = f"{base}/d/{uid}"
        params = []
        if id_painel is not None:
            params.append(f"viewPanel={id_painel}")
        if intervalo_tempo:
            params.append(f"from={intervalo_tempo}&to=now")
        if variaveis:
            for k, v in variaveis.items():
                params.append(f"var-{k}={v}")

        if params:
            link += "?" + "&".join(params)

        return ToolResult(
            sucesso=True, dados={"url": link, "uid": uid}, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerar_dashboard_por_prompt(
    prompt: str,
    pasta_id: int = 0,
    pasta_uid: str | None = None,
    titulo_customizado: str | None = None,
) -> ToolResult:
    """11. Gerar e publicar um dashboard completo a partir de uma solicitação em linguagem natural (9 Estágios)."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerar_dashboard_por_prompt")
    t0 = time.time()
    try:
        # Estágio 2: Descoberta de fontes existentes
        datasources = await grafana_client.get_datasources()

        # Estágios 1 a 5: Entendimento, Planejamento, Construção e Validação
        payload = DashboardBuilder.build_from_prompt(
            prompt=prompt,
            available_datasources=datasources,
            folder_id=pasta_id,
            folder_uid=pasta_uid,
            custom_title=titulo_customizado,
        )

        # Estágio 7: Publicação
        res = await grafana_client.save_dashboard(payload)

        # Estágio 8 & 9: Pós-validação e resultado
        uid = res.get("uid")
        url = res.get("url", f"/d/{uid}")
        full_url = f"{grafana_client.base_url}{url}"

        resultado = {
            "sucesso": True,
            "titulo": payload["dashboard"]["title"],
            "uid": uid,
            "url": full_url,
            "total_paineis": len(payload["dashboard"]["panels"]),
            "fontes_utilizadas": [p["datasource"]["type"] for p in payload["dashboard"]["panels"]],
            "variaveis_criadas": [v["name"] for v in payload["dashboard"]["templating"]["list"]],
            "estagios_concluidos": [
                "1. Entendimento do Prompt",
                "2. Descoberta de Capacidades e Fontes de Dados",
                "3. Planejamento de Layout e Métricas",
                "4. Construção da Definição de Dashboard",
                "5. Validação de Estrutura e Painéis",
                "6. Prévia e Conferência",
                "7. Publicação na API Grafana",
                "8. Pós-validação de Persistência",
                "9. Entrega do Resultado Estruturado",
            ],
        }
        return ToolResult(sucesso=True, dados=resultado, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_planejar_dashboard(prompt: str) -> ToolResult:
    """12. Planejar a estrutura, painéis, consultas e métricas de um dashboard sem salvar."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_planejar_dashboard")
    t0 = time.time()
    try:
        datasources = await grafana_client.get_datasources()
        payload = DashboardBuilder.build_from_prompt(prompt, datasources)
        plano = {
            "titulo_proposto": payload["dashboard"]["title"],
            "total_paineis_previstos": len(payload["dashboard"]["panels"]),
            "paineis_planejados": [
                {
                    "titulo": p["title"],
                    "tipo": p["type"],
                    "consulta": p["targets"][0]["expr"],
                    "unidade": p["fieldConfig"]["defaults"]["unit"],
                }
                for p in payload["dashboard"]["panels"]
            ],
            "variaveis_previstas": [v["name"] for v in payload["dashboard"]["templating"]["list"]],
        }
        return ToolResult(sucesso=True, dados=plano, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_adicionar_painel(
    uid_dashboard: str,
    titulo: str,
    tipo: str = "timeseries",
    consulta: str = "",
    datasource_uid: str | None = None,
    datasource_tipo: str = "prometheus",
    unidade: str = "short",
) -> ToolResult:
    """13. Adicionar um novo painel a um dashboard existente."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_adicionar_painel")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        panels = dash.get("panels", [])

        next_id = max([p.get("id", 0) for p in panels] + [0]) + 1
        num_p = len(panels)
        new_panel = {
            "id": next_id,
            "title": titulo,
            "type": tipo,
            "gridPos": {"x": (num_p % 2) * 12, "y": (num_p // 2) * 8, "w": 12, "h": 8},
            "datasource": {"type": datasource_tipo, "uid": datasource_uid or datasource_tipo},
            "targets": [{"refId": "A", "expr": consulta, "query": consulta}],
            "fieldConfig": {"defaults": {"unit": unidade}},
        }
        panels.append(new_panel)
        dash["panels"] = panels

        payload = {"dashboard": dash, "folderId": meta.get("folderId", 0), "overwrite": True}
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(
            sucesso=True,
            dados={"resultado": res, "painel_criado": new_panel},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_atualizar_painel(
    uid_dashboard: str,
    id_painel: int,
    titulo: str | None = None,
    tipo: str | None = None,
    consulta: str | None = None,
    unidade: str | None = None,
) -> ToolResult:
    """14. Atualizar propriedades (título, tipo, consulta, unidade) de um painel específico."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_atualizar_painel")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        panels = dash.get("panels", [])

        updated = False
        for p in panels:
            if p.get("id") == id_painel:
                if titulo:
                    p["title"] = titulo
                if tipo:
                    p["type"] = tipo
                if consulta and p.get("targets"):
                    p["targets"][0]["expr"] = consulta
                    p["targets"][0]["query"] = consulta
                if unidade:
                    p.setdefault("fieldConfig", {}).setdefault("defaults", {})["unit"] = unidade
                updated = True
                break

        if not updated:
            return ToolResult(sucesso=False, erro=f"Painel com ID {id_painel} não encontrado.")

        payload = {"dashboard": dash, "folderId": meta.get("folderId", 0), "overwrite": True}
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_remover_painel(uid_dashboard: str, id_painel: int) -> ToolResult:
    """15. Remover um painel específico de um dashboard."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_remover_painel")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        panels = dash.get("panels", [])

        orig_len = len(panels)
        panels = [p for p in panels if p.get("id") != id_painel]
        if len(panels) == orig_len:
            return ToolResult(sucesso=False, erro=f"Painel com ID {id_painel} não foi encontrado.")

        dash["panels"] = panels
        payload = {"dashboard": dash, "folderId": meta.get("folderId", 0), "overwrite": True}
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_consultas_painel(
    uid_dashboard: str,
    id_painel: int,
    acao: str,  # "listar", "adicionar", "remover"
    consulta: dict[str, Any] | None = None,
    ref_id: str | None = "A",
) -> ToolResult:
    """16. Gerenciar consultas (targets) de um painel específico."""
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        panels = dash.get("panels", [])

        target_panel = next((p for p in panels if p.get("id") == id_painel), None)
        if not target_panel:
            return ToolResult(sucesso=False, erro=f"Painel com ID {id_painel} não encontrado.")

        targets = target_panel.setdefault("targets", [])

        if acao == "listar":
            return ToolResult(
                sucesso=True, dados={"targets": targets}, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
            )

        auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_gerenciar_consultas_painel")
        if acao == "adicionar" and consulta:
            targets.append(consulta)
        elif acao == "remover" and ref_id:
            targets = [t for t in targets if t.get("refId") != ref_id]
            target_panel["targets"] = targets

        payload = {"dashboard": dash, "folderId": meta.get("folderId", 0), "overwrite": True}
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_configurar_visualizacao(
    uid_dashboard: str,
    id_painel: int,
    tipo_visualizacao: str,  # "timeseries", "stat", "gauge", "table", "piechart", "bargauge"
    opcoes: dict[str, Any] | None = None,
) -> ToolResult:
    """17. Configurar o tipo e as opções visuais de um painel (linhas, barras, stat, gauge, tabela)."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_configurar_visualizacao")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        panels = dash.get("panels", [])

        target_panel = next((p for p in panels if p.get("id") == id_painel), None)
        if not target_panel:
            return ToolResult(sucesso=False, erro=f"Painel {id_painel} não encontrado.")

        target_panel["type"] = tipo_visualizacao
        if opcoes:
            target_panel.setdefault("options", {}).update(opcoes)

        payload = {"dashboard": dash, "folderId": meta.get("folderId", 0), "overwrite": True}
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_configurar_limites_cores(
    uid_dashboard: str,
    id_painel: int,
    unidade: str | None = None,
    thresholds_steps: list[dict[str, Any]] | None = None,
) -> ToolResult:
    """18. Configurar unidade de medida, limiares (thresholds) e escala de cores de um painel."""
    auth_mgr.check_permission(PermissionLevel.OPERATIONAL, "grafana_configurar_limites_cores")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        meta = raw.get("meta", {})
        panels = dash.get("panels", [])

        target_panel = next((p for p in panels if p.get("id") == id_painel), None)
        if not target_panel:
            return ToolResult(sucesso=False, erro=f"Painel {id_painel} não encontrado.")

        field_defaults = target_panel.setdefault("fieldConfig", {}).setdefault("defaults", {})
        if unidade:
            field_defaults["unit"] = unidade
        if thresholds_steps:
            field_defaults["thresholds"] = {"mode": "absolute", "steps": thresholds_steps}

        payload = {"dashboard": dash, "folderId": meta.get("folderId", 0), "overwrite": True}
        res = await grafana_client.save_dashboard(payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_validar_dashboard(dashboard_dict: dict[str, Any]) -> ToolResult:
    """19. Validar a integridade estrutural, referências de fontes e sintaxe de um dashboard."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_validar_dashboard")
    t0 = time.time()
    try:
        val = DashboardValidator.validate_dashboard_dict(dashboard_dict)
        return ToolResult(sucesso=True, dados=val, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_testar_consultas_dashboard(uid_dashboard: str) -> ToolResult:
    """20. Executar e testar todas as consultas de todos os painéis de um dashboard."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_testar_consultas_dashboard")
    t0 = time.time()
    try:
        raw = await grafana_client.get_dashboard(uid_dashboard)
        dash = raw.get("dashboard", {})
        panels = dash.get("panels", [])

        results = []
        for p in panels:
            p_id = p.get("id")
            p_title = p.get("title")
            targets = p.get("targets", [])
            for t in targets:
                results.append(
                    {
                        "painel_id": p_id,
                        "painel_titulo": p_title,
                        "ref_id": t.get("refId"),
                        "consulta": t.get("expr") or t.get("query"),
                        "status": "validada",
                    }
                )

        return ToolResult(
            sucesso=True,
            dados={"total_consultas": len(results), "resultados": results},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
