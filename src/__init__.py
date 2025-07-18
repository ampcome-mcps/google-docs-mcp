"""Google Docs MCP Server package."""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "A Model Context Protocol server for Google Docs API with structured output and Nango authentication"

from .models import (
    DocumentResponse,
    BatchUpdateResponse, 
    CreateDocumentResponse,
    NangoCredentials,
    ErrorResponse
)

from .auth import get_connection_credentials, get_auth_headers
from .api_client import make_request, get_document_api, create_document_api, batch_update_document_api
from .tools import register_tools

__all__ = [
    "DocumentResponse",
    "BatchUpdateResponse", 
    "CreateDocumentResponse",
    "NangoCredentials",
    "ErrorResponse",
    "get_connection_credentials",
    "get_auth_headers",
    "make_request",
    "get_document_api",
    "create_document_api",
    "batch_update_document_api",
    "register_tools"
]
