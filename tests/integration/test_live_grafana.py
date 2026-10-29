"""Testes de integração contra a instância real do Grafana (192.168.0.107:3000)."""

import pytest

from grafana_mcp.tools import (
    grafana_auditar_configuracoes,
    grafana_listar_fontes_dados,
    grafana_obter_informacoes_instancia,
    grafana_testar_conexao,
)


@pytest.mark.asyncio
async def test_live_conexao_e_saude():
    """Valida conectividade e autenticação com o Grafana real."""
    res = await grafana_testar_conexao()
    assert res.sucesso is True
    assert res.dados["status"] == "CONECTADO COM SUCESSO"
    assert "versao_grafana" in res.dados


@pytest.mark.asyncio
async def test_live_informacoes_instancia():
    """Valida obtenção da versão e status do banco do Grafana."""
    res = await grafana_obter_informacoes_instancia()
    assert res.sucesso is True
    assert res.dados["status_banco"] == "ok"
    assert res.dados["versao"] != "desconhecida"


@pytest.mark.asyncio
async def test_live_listar_fontes_dados():
    """Valida listagem de datasources configuradas."""
    res = await grafana_listar_fontes_dados()
    assert res.sucesso is True
    assert "fontes_dados" in res.dados
    assert isinstance(res.dados["fontes_dados"], list)


@pytest.mark.asyncio
async def test_live_auditoria_configuracoes():
    """Valida execução da auditoria de segurança da instância."""
    res = await grafana_auditar_configuracoes()
    assert res.sucesso is True
    assert "pontuacao_conformidade" in res.dados
