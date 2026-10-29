"""Cliente HTTP assíncrono para a API REST do Grafana."""

import asyncio
from typing import Any

import httpx

from .api_compatibility import GrafanaCapabilities
from .auth import GrafanaAuth
from .config import settings
from .exceptions import (
    GrafanaAuthError,
    GrafanaConnectionError,
    GrafanaMCPError,
    GrafanaNotFoundError,
    GrafanaPermissionError,
    GrafanaValidationError,
)


class GrafanaClient:
    """Cliente centralizado assíncrono para todas as chamadas à API do Grafana."""

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
        user: str | None = None,
        password: str | None = None,
        org_id: int | None = None,
        verify_tls: bool | None = None,
        timeout: float | None = None,
    ) -> None:
        self.base_url = (base_url or settings.clean_grafana_url).rstrip("/")
        self.auth = GrafanaAuth(
            token=token or settings.grafana_api_token,
            user=user or settings.grafana_user,
            password=password or settings.grafana_password,
            org_id=org_id if org_id is not None else settings.grafana_org_id,
        )
        self.verify_tls = verify_tls if verify_tls is not None else settings.grafana_verify_tls
        self.timeout = timeout if timeout is not None else settings.grafana_timeout
        self.capabilities = GrafanaCapabilities()
        self._semaphore: asyncio.Semaphore | None = None
        self._client: httpx.AsyncClient | None = None

    def _get_semaphore(self) -> asyncio.Semaphore:
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(settings.grafana_max_concurrent_queries)
        return self._semaphore

    async def get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                verify=self.verify_tls,
                timeout=httpx.Timeout(self.timeout),
                headers=self.auth.get_headers(),
            )
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        retries: int = 2,
    ) -> Any:
        """Executa uma requisição HTTP à API Grafana com tratamento de erros e retries."""
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}/{endpoint.lstrip('/')}"
        sem = self._get_semaphore()

        merged_headers = self.auth.get_headers()
        if headers:
            merged_headers.update(headers)

        last_error: Exception | None = None

        async with sem:
            for attempt in range(retries + 1):
                client = await self.get_client()
                try:
                    resp = await client.request(
                        method=method,
                        url=url,
                        params=params,
                        json=json_data,
                        headers=merged_headers,
                    )

                    if resp.status_code in (200, 201, 202):
                        if "application/json" in resp.headers.get("Content-Type", ""):
                            return resp.json()
                        return resp.text

                    if resp.status_code == 401:
                        raise GrafanaAuthError(
                            "Falha de autenticação no Grafana: Token ou credenciais inválidos ou expirados.",
                            details={"status": 401, "body": resp.text[:200]},
                        )
                    if resp.status_code == 403:
                        raise GrafanaPermissionError(
                            "Acesso negado no Grafana: Permissão insuficiente para este recurso.",
                            details={"status": 403, "body": resp.text[:200]},
                        )
                    if resp.status_code == 404:
                        raise GrafanaNotFoundError(
                            f"Recurso não encontrado no Grafana: {endpoint}",
                            details={"status": 404, "body": resp.text[:200]},
                        )
                    if resp.status_code in (400, 422):
                        raise GrafanaValidationError(
                            f"Requisição inválida enviada ao Grafana: {resp.text[:300]}",
                            details={"status": resp.status_code, "body": resp.text[:300]},
                        )

                    # Códigos transitórios (502, 503, 504) tentam retry
                    if resp.status_code in (502, 503, 504) and attempt < retries:
                        await asyncio.sleep(0.5 * (attempt + 1))
                        continue

                    raise GrafanaMCPError(
                        f"Erro HTTP {resp.status_code} na API Grafana: {resp.text[:200]}",
                        details={"status": resp.status_code, "body": resp.text[:200]},
                    )

                except httpx.ConnectError as e:
                    last_error = GrafanaConnectionError(
                        f"Não foi possível conectar ao Grafana em '{self.base_url}': Verifique se o servidor está ativo.",
                        details=str(e),
                    )
                except httpx.TimeoutException as e:
                    last_error = GrafanaConnectionError(
                        f"Timeout aguardando resposta da API Grafana ({self.timeout}s): {endpoint}",
                        details=str(e),
                    )
                except (GrafanaAuthError, GrafanaPermissionError, GrafanaNotFoundError, GrafanaValidationError):
                    raise
                except Exception as e:
                    last_error = e

                if attempt < retries:
                    await asyncio.sleep(0.5 * (attempt + 1))

        if last_error:
            if isinstance(last_error, GrafanaMCPError):
                raise last_error
            raise GrafanaMCPError(f"Falha na comunicação com o Grafana: {last_error}", details=str(last_error))

    async def get_health(self) -> dict[str, Any]:
        """Obtém saúde e versão do Grafana via /api/health."""
        data = await self.request("GET", "/api/health")
        if isinstance(data, dict):
            self.capabilities = GrafanaCapabilities(data)
        return data

    async def search_resources(
        self,
        query: str | None = None,
        tag: str | None = None,
        type_: str | None = None,
        folder_ids: list[int] | None = None,
        limit: int = 100,
        page: int = 1,
    ) -> list[dict[str, Any]]:
        """Pesquisa dashboards, pastas e recursos via /api/search."""
        params: dict[str, Any] = {"limit": limit, "page": page}
        if query:
            params["query"] = query
        if tag:
            params["tag"] = tag
        if type_:
            params["type"] = type_
        if folder_ids:
            params["folderIds"] = folder_ids

        data = await self.request("GET", "/api/search", params=params)
        return data if isinstance(data, list) else []

    async def get_dashboard(self, uid: str) -> dict[str, Any]:
        """Recupera a definição completa de um dashboard pelo UID."""
        return await self.request("GET", f"/api/dashboards/uid/{uid}")

    async def save_dashboard(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Cria ou atualiza um dashboard via /api/dashboards/db."""
        return await self.request("POST", "/api/dashboards/db", json_data=payload)

    async def delete_dashboard(self, uid: str) -> dict[str, Any]:
        """Exclui um dashboard pelo UID."""
        return await self.request("DELETE", f"/api/dashboards/uid/{uid}")

    async def get_datasources(self) -> list[dict[str, Any]]:
        """Lista todas as fontes de dados via /api/datasources."""
        data = await self.request("GET", "/api/datasources")
        return data if isinstance(data, list) else []

    async def get_datasource_by_uid(self, uid: str) -> dict[str, Any]:
        """Recupera detalhes de uma fonte de dados pelo UID."""
        return await self.request("GET", f"/api/datasources/uid/{uid}")

    async def query_datasource(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Executa consultas unificadas através do endpoint /api/ds/query."""
        return await self.request("POST", "/api/ds/query", json_data=payload)


# Instância global reutilizável
grafana_client = GrafanaClient()
