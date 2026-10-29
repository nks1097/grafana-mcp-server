"""Utilitário de paginação e limitação de resultados para consultas da API Grafana."""

from typing import Any


def paginate_results(items: list[Any], limit: int = 100, page: int = 1) -> tuple[list[Any], bool, int]:
    """
    Aplica paginação local com segurança sobre uma lista de itens.
    Retorna (itens_paginados, truncado, total_itens).
    """
    total = len(items)
    if limit <= 0:
        limit = 100
    if page <= 0:
        page = 1

    start = (page - 1) * limit
    end = start + limit

    paginated = items[start:end]
    truncated = end < total

    return paginated, truncated, total
