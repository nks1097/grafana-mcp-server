"""Modelos de dados Pydantic e envelopes padronizados do Grafana MCP Server."""

from typing import Any

from pydantic import BaseModel, Field


class ToolMetadata(BaseModel):
    """Metadados de execução da ferramenta MCP."""

    duracao_ms: float = Field(default=0.0, description="Duração da operação em milissegundos")
    truncado: bool = Field(default=False, description="Indica se os dados foram truncados por limite")
    total_registros: int | None = Field(default=None, description="Total de registros encontrados")
    versao_grafana: str | None = Field(default=None, description="Versão do Grafana conectada")
    somente_leitura: bool = Field(default=False, description="Estado do modo de proteção somente leitura")


class ToolResult(BaseModel):
    """Envelope padrão de resposta para todas as 100 ferramentas do Grafana MCP."""

    sucesso: bool = Field(default=True, description="Indica se a operação foi bem-sucedida")
    dados: Any = Field(default=None, description="Carga útil da resposta estruturada")
    erro: str | None = Field(default=None, description="Mensagem de erro amigável caso haja falha")
    avisos: list[str] = Field(default_factory=list, description="Lista de alertas e avisos operacionais")
    id_requisicao: str | None = Field(default=None, description="Identificador único da operação")
    metadados: ToolMetadata = Field(default_factory=ToolMetadata, description="Metadados da execução")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class DashboardSummary(BaseModel):
    """Resumo de metadados de um dashboard do Grafana."""

    id: int
    uid: str
    title: str
    uri: str | None = None
    url: str | None = None
    slug: str | None = None
    type: str = "dash-db"
    tags: list[str] = Field(default_factory=list)
    isStarred: bool = False
    folderId: int | None = None
    folderUid: str | None = None
    folderTitle: str | None = None


class DatasourceSummary(BaseModel):
    """Resumo de fonte de dados do Grafana."""

    id: int
    uid: str
    name: str
    type: str
    typeLogoUrl: str | None = None
    access: str = "proxy"
    url: str | None = None
    isDefault: bool = False
    readOnly: bool = False


class QueryResult(BaseModel):
    """Resultado estruturado de execução de consulta de métrica, log ou trace."""

    refId: str
    status: str = "success"
    series_count: int = 0
    records_count: int = 0
    data: Any = None
    error: str | None = None
