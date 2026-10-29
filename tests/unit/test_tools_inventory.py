"""Testes de inventário e conformidade das 100 ferramentas do Grafana MCP Server."""

import inspect

from grafana_mcp.tools import ALL_TOOLS, TOOLS_BY_NAME


def test_total_ferramentas_cadastradas():
    """Garante que exatamente 100 ferramentas estão cadastradas e exportadas."""
    assert len(ALL_TOOLS) == 100, f"Esperado 100 ferramentas, encontrado {len(ALL_TOOLS)}"
    assert len(TOOLS_BY_NAME) == 100, f"Esperado 100 nomes únicos no dicionário, encontrado {len(TOOLS_BY_NAME)}"


def test_padrao_nomenclatura_ferramentas():
    """Garante que todas as ferramentas seguem o padrão snake_case com prefixo 'grafana_'."""
    for tool_fn in ALL_TOOLS:
        nome = tool_fn.__name__
        assert nome.startswith("grafana_"), f"Ferramenta '{nome}' não inicia com prefixo 'grafana_'"
        assert nome.islower(), f"Ferramenta '{nome}' deve ser totalmente minúscula"
        assert " " not in nome and "-" not in nome, f"Ferramenta '{nome}' deve usar apenas underscore"


def test_presenca_docstring_portugues():
    """Garante que todas as ferramentas possuem documentação e número/descrição."""
    for tool_fn in ALL_TOOLS:
        doc = tool_fn.__doc__
        assert doc is not None and len(doc.strip()) > 10, f"Ferramenta '{tool_fn.__name__}' não possui docstring válida"


def test_funcoes_assincronas():
    """Garante que todas as 100 ferramentas são corrotinas assíncronas (async def)."""
    for tool_fn in ALL_TOOLS:
        assert inspect.iscoroutinefunction(tool_fn), f"Ferramenta '{tool_fn.__name__}' não é assíncrona (async def)"
