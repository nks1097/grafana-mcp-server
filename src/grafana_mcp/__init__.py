"""Grafana MCP Server - Servidor MCP corporativo com 100 ferramentas em português."""

__version__ = "1.0.0"
__author__ = "Natanael Krindges"

from .config import settings
from .models import ToolResult

__all__ = ["ToolResult", "__version__", "settings"]
