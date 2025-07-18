"""Google Docs MCP Server - Structured output models."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """Response structure for document operations."""
    documentId: str = Field(description="The ID of the document")
    title: str = Field(description="The title of the document")
    body: Optional[Dict[str, Any]] = Field(default=None, description="The document body content")
    revisionId: Optional[str] = Field(default=None, description="The revision ID of the document")
    suggestionsViewMode: Optional[str] = Field(default=None, description="The suggestions view mode")
    namedRanges: Optional[Dict[str, Any]] = Field(default=None, description="Named ranges in the document")
    lists: Optional[Dict[str, Any]] = Field(default=None, description="Lists in the document")
    documentStyle: Optional[Dict[str, Any]] = Field(default=None, description="The document style")
    footers: Optional[Dict[str, Any]] = Field(default=None, description="Document footers")
    headers: Optional[Dict[str, Any]] = Field(default=None, description="Document headers")
    footnotes: Optional[Dict[str, Any]] = Field(default=None, description="Document footnotes")
    inlineObjects: Optional[Dict[str, Any]] = Field(default=None, description="Inline objects in the document")
    positionedObjects: Optional[Dict[str, Any]] = Field(default=None, description="Positioned objects in the document")


class BatchUpdateResponse(BaseModel):
    """Response structure for batch update operations."""
    documentId: str = Field(description="The ID of the updated document")
    writeControl: Optional[Dict[str, Any]] = Field(default=None, description="Write control information")
    replies: Optional[List[Dict[str, Any]]] = Field(default=None, description="Replies to the update requests")


class CreateDocumentResponse(BaseModel):
    """Response structure for document creation."""
    documentId: str = Field(description="The ID of the created document")
    title: str = Field(description="The title of the created document")
    revisionId: str = Field(description="The revision ID of the created document")
    body: Optional[Dict[str, Any]] = Field(default=None, description="The document body content")


class NangoCredentials(BaseModel):
    """Nango connection credentials structure."""
    connection_id: str = Field(description="The Nango connection ID")
    provider_config_key: str = Field(description="The provider configuration key")
    credentials: Dict[str, Any] = Field(description="The OAuth credentials")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional connection metadata")


class ErrorResponse(BaseModel):
    """Error response structure."""
    error: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
    details: Optional[str] = Field(default=None, description="Additional error details")
