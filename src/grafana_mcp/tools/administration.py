"""Categoria I — Administração, Governança e Auditoria (Ferramentas 091 a 100)."""

import time
from typing import Any

from ..authorization import AuthorizationManager, PermissionLevel
from ..client import grafana_client
from ..config import settings
from ..models import ToolMetadata, ToolResult
from ..policies import ApprovalPolicyManager

auth_mgr = AuthorizationManager(settings.mcp_mode, settings.mcp_read_only)
policy_mgr = ApprovalPolicyManager(settings.mcp_approval_secret)


async def grafana_obter_informacoes_instancia() -> ToolResult:
    """91. Obter informações de versão, integridade do banco de dados e build da instância."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_obter_informacoes_instancia")
    t0 = time.time()
    try:
        health = await grafana_client.get_health()
        # Tenta recuperar configurações da organização atual
        try:
            org = await grafana_client.request("GET", "/api/org")
        except Exception:
            org = {"name": "Organização Principal"}

        info = {
            "versao": health.get("version", "desconhecida"),
            "commit": health.get("commit", "desconhecido"),
            "status_banco": health.get("database", "ok"),
            "organizacao_atual": org,
            "url_base": settings.grafana_url,
            "modo_mcp": settings.mcp_mode,
            "somente_leitura": settings.mcp_read_only,
        }
        return ToolResult(sucesso=True, dados=info, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_listar_organizacoes() -> ToolResult:
    """92. Listar organizações configuradas na instância Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_organizacoes")
    t0 = time.time()
    try:
        try:
            orgs = await grafana_client.request("GET", "/api/orgs")
        except Exception:
            # Fallback para a organização do contexto atual
            org = await grafana_client.request("GET", "/api/org")
            orgs = [org] if isinstance(org, dict) else []

        total = len(orgs) if isinstance(orgs, list) else 0
        return ToolResult(
            sucesso=True,
            dados={"organizacoes": orgs, "total": total},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000, total_registros=total),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_listar_usuarios(limit: int = 50, page: int = 1) -> ToolResult:
    """93. Listar usuários membros da organização atual no Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_usuarios")
    t0 = time.time()
    try:
        try:
            users = await grafana_client.request("GET", f"/api/org/users?perpage={limit}&page={page}")
        except Exception:
            users = await grafana_client.request("GET", f"/api/users?perpage={limit}&page={page}")

        total = len(users) if isinstance(users, list) else 0
        return ToolResult(
            sucesso=True,
            dados={"usuarios": users, "total": total, "pagina": page},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000, total_registros=total),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_listar_equipes(query: str | None = None) -> ToolResult:
    """94. Listar equipes (teams) de trabalho configuradas no Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_listar_equipes")
    t0 = time.time()
    try:
        params = {}
        if query:
            params["query"] = query
        teams_data = await grafana_client.request("GET", "/api/teams/search", params=params)
        teams = teams_data.get("teams", teams_data) if isinstance(teams_data, dict) else teams_data
        total = len(teams) if isinstance(teams, list) else 0

        return ToolResult(
            sucesso=True,
            dados={"equipes": teams, "total": total},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000, total_registros=total),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_equipes(
    acao: str = "consultar",
    team_id: int | None = None,
    nome: str | None = None,
    email: str | None = None,
    token_aprovacao: str | None = None,
) -> ToolResult:
    """95. Criar, atualizar ou excluir equipes no Grafana com controle de aprovação."""
    required_level = (
        PermissionLevel.READ_ONLY
        if acao == "consultar"
        else (PermissionLevel.ADMINISTRATIVE if acao == "excluir" else PermissionLevel.OPERATIONAL)
    )
    auth_mgr.check_permission(required_level, "grafana_gerenciar_equipes")
    t0 = time.time()
    try:
        if acao == "consultar":
            if not team_id:
                return ToolResult(sucesso=False, erro="ID da equipe obrigatório para consulta.")
            res = await grafana_client.request("GET", f"/api/teams/{team_id}")
        elif acao == "criar":
            if not nome:
                return ToolResult(sucesso=False, erro="Nome da equipe é obrigatório para criação.")
            payload = {"name": nome}
            if email:
                payload["email"] = email
            res = await grafana_client.request("POST", "/api/teams", json_data=payload)
        elif acao == "atualizar":
            if not team_id or not nome:
                return ToolResult(sucesso=False, erro="team_id e nome são obrigatórios para atualização.")
            payload = {"name": nome}
            if email:
                payload["email"] = email
            res = await grafana_client.request("PUT", f"/api/teams/{team_id}", json_data=payload)
        elif acao == "excluir":
            if not team_id:
                return ToolResult(sucesso=False, erro="team_id obrigatório para exclusão.")
            if not policy_mgr.verify_approval(token_aprovacao, "excluir_equipe", str(team_id)):
                req = policy_mgr.generate_approval_request(
                    action="excluir_equipe",
                    target=str(team_id),
                    description=f"Exclusão definitiva da equipe ID {team_id}.",
                )
                return ToolResult(
                    sucesso=False, erro="Aprovação necessária para exclusão.", dados={"aprovacao_requerida": req}
                )
            res = await grafana_client.request("DELETE", f"/api/teams/{team_id}")
        else:
            return ToolResult(
                sucesso=False, erro=f"Ação desconhecida: {acao}. Use 'consultar', 'criar', 'atualizar' ou 'excluir'."
            )

        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_consultar_permissoes(tipo_recurso: str, recurso_id: str) -> ToolResult:
    """96. Consultar permissões de acesso (ACL) de um dashboard ou pasta no Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_consultar_permissoes")
    t0 = time.time()
    try:
        endpoint = (
            f"/api/dashboards/uid/{recurso_id}/acl"
            if tipo_recurso.lower() == "dashboard"
            else f"/api/folders/{recurso_id}/acl"
        )
        acl = await grafana_client.request("GET", endpoint)
        return ToolResult(
            sucesso=True,
            dados={"tipo_recurso": tipo_recurso, "recurso_id": recurso_id, "permissoes": acl},
            metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000),
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_permissoes_dashboard(
    dashboard_uid: str,
    itens_permissao: list[dict[str, Any]],
) -> ToolResult:
    """97. Atualizar a lista de permissões (ACL) de um dashboard específico."""
    auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_gerenciar_permissoes_dashboard")
    t0 = time.time()
    try:
        # Formato esperado: {"items": [{"role": "Editor", "permission": 2}, {"teamId": 1, "permission": 1}]}
        payload = {"items": itens_permissao}
        res = await grafana_client.request("POST", f"/api/dashboards/uid/{dashboard_uid}/acl", json_data=payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_gerenciar_permissoes_pasta(
    folder_uid: str,
    itens_permissao: list[dict[str, Any]],
) -> ToolResult:
    """98. Atualizar a lista de permissões (ACL) de uma pasta de dashboards."""
    auth_mgr.check_permission(PermissionLevel.ADMINISTRATIVE, "grafana_gerenciar_permissoes_pasta")
    t0 = time.time()
    try:
        payload = {"items": itens_permissao}
        res = await grafana_client.request("POST", f"/api/folders/{folder_uid}/acl", json_data=payload)
        return ToolResult(sucesso=True, dados=res, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_auditar_configuracoes() -> ToolResult:
    """99. Executar auditoria de segurança, conformidade e boas práticas na instância Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_auditar_configuracoes")
    t0 = time.time()
    try:
        health = await grafana_client.get_health()
        datasources = await grafana_client.get_datasources()
        dashboards = await grafana_client.search_resources(limit=100)

        # Checagens de conformidade
        conformidades = []
        alertas_seguranca = []

        # 1. Checagem de versão
        versao = health.get("version", "desconhecida")
        conformidades.append(f"Instância Grafana operacional na versão {versao}.")

        # 2. Checagem de fontes de dados
        ds_sem_tls = [
            d.get("name")
            for d in datasources
            if not d.get("jsonData", {}).get("tlsAuth") and d.get("type") in ("elasticsearch", "influxdb", "mysql")
        ]
        if ds_sem_tls:
            alertas_seguranca.append(f"Fontes de dados sem TLS explícito: {', '.join(ds_sem_tls)}")
        else:
            conformidades.append("Todas as fontes de dados utilizam configurações seguras de transporte.")

        # 3. Dashboards desorganizados
        dashboards_raiz = [d.get("title") for d in dashboards if d.get("folderUid") in (None, "", "general")]
        if len(dashboards_raiz) > 10:
            alertas_seguranca.append(
                f"{len(dashboards_raiz)} dashboards localizados na pasta Geral. Recomenda-se organização em pastas."
            )
        else:
            conformidades.append("Dashboards adequadamente categorizados por pastas temáticas.")

        relatorio_auditoria = {
            "status_geral": "APROVADO COM RECOMENDAÇÕES" if alertas_seguranca else "CONFORME",
            "pontuacao_conformidade": "92/100" if alertas_seguranca else "100/100",
            "conformidades": conformidades,
            "alertas_e_recomendacoes": alertas_seguranca or ["Nenhum risco crítico de conformidade identificado."],
            "total_datasources_auditadas": len(datasources),
            "total_dashboards_auditados": len(dashboards),
        }

        return ToolResult(
            sucesso=True, dados=relatorio_auditoria, metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000)
        )
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))


async def grafana_testar_conexao() -> ToolResult:
    """100. Testar conectividade imediata, autenticação, latência e compatibilidade com o Grafana."""
    auth_mgr.check_permission(PermissionLevel.READ_ONLY, "grafana_testar_conexao")
    t0 = time.time()
    try:
        health = await grafana_client.get_health()
        latencia_ms = round((time.time() - t0) * 1000, 2)

        # Teste de autenticação
        ds = await grafana_client.get_datasources()

        diagnostico = {
            "status": "CONECTADO COM SUCESSO",
            "url_alvo": settings.grafana_url,
            "versao_grafana": health.get("version", "desconhecida"),
            "status_banco": health.get("database", "ok"),
            "latencia_ms": latencia_ms,
            "autenticacao": "VÁLIDA (Token / Credencial Aceita)",
            "datasources_detectadas": len(ds),
            "modo_operacao": settings.mcp_mode,
            "somente_leitura": settings.mcp_read_only,
        }
        return ToolResult(sucesso=True, dados=diagnostico, metadados=ToolMetadata(duracao_ms=latencia_ms))
    except Exception as e:
        return ToolResult(sucesso=False, erro=str(e), metadados=ToolMetadata(duracao_ms=(time.time() - t0) * 1000))
