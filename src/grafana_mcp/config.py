"""Configurações e variáveis de ambiente do Grafana MCP Server."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_PATH = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_ENV_PATH if _ENV_PATH.exists() else ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Conexão com Grafana
    grafana_url: str = Field(default="http://192.168.0.107:3000", alias="GRAFANA_URL")
    grafana_api_token: str | None = Field(default=None, alias="GRAFANA_API_TOKEN")
    grafana_user: str = Field(default="admin", alias="GRAFANA_USER")
    grafana_password: str | None = Field(default=None, alias="GRAFANA_PASSWORD")
    grafana_org_id: int = Field(default=1, alias="GRAFANA_ORG_ID")

    # Rede, TLS e limites
    grafana_verify_tls: bool = Field(default=False, alias="GRAFANA_VERIFY_TLS")
    grafana_ca_bundle: str | None = Field(default=None, alias="GRAFANA_CA_BUNDLE")
    grafana_timeout: float = Field(default=30.0, alias="GRAFANA_TIMEOUT")
    grafana_max_results: int = Field(default=100, alias="GRAFANA_MAX_RESULTS")
    grafana_max_concurrent_queries: int = Field(default=10, alias="GRAFANA_MAX_CONCURRENT_QUERIES")
    grafana_default_time_range: str = Field(default="now-6h", alias="GRAFANA_DEFAULT_TIME_RANGE")

    # Renderização de imagem
    grafana_rendering_enabled: bool = Field(default=False, alias="GRAFANA_RENDERING_ENABLED")
    grafana_rendering_url: str | None = Field(default=None, alias="GRAFANA_RENDERING_URL")

    # MCP e Transporte
    mcp_transport: str = Field(default="stdio", alias="MCP_TRANSPORT")
    mcp_host: str = Field(default="0.0.0.0", alias="MCP_HOST")
    mcp_port: int = Field(default=8001, alias="MCP_PORT")
    mcp_auth_mode: str = Field(default="token", alias="MCP_AUTH_MODE")

    # Governança e RBAC
    mcp_read_only: bool = Field(default=False, alias="MCP_READ_ONLY")
    mcp_mode: str = Field(default="operacional", alias="MCP_MODE")  # somente_leitura, operacional, administrativo
    mcp_require_approval_destructive: bool = Field(default=True, alias="MCP_REQUIRE_APPROVAL_DESTRUCTIVE")
    mcp_approval_secret: str = Field(default="chave-secreta-grafana-mcp-2026", alias="MCP_APPROVAL_SECRET")

    # Auditoria e Relatórios
    mcp_audit_enabled: bool = Field(default=True, alias="MCP_AUDIT_ENABLED")
    mcp_audit_path: str = Field(default="./audit_grafana_mcp.jsonl", alias="MCP_AUDIT_PATH")
    mcp_report_output_dir: str = Field(default="./reports_output", alias="MCP_REPORT_OUTPUT_DIR")
    mcp_max_report_size: str = Field(default="50MB", alias="MCP_MAX_REPORT_SIZE")

    @property
    def clean_grafana_url(self) -> str:
        return self.grafana_url.rstrip("/")


settings = Settings()
