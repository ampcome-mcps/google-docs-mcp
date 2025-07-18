"""MCP Tools for Google Docs operations."""

from typing import List, Dict, Any, Optional

from mcp.server.fastmcp import FastMCP

from .models import (
    DocumentResponse, 
    CreateDocumentResponse, 
    BatchUpdateResponse,
    NangoCredentials
)
from .api_client import get_document_api, create_document_api, batch_update_document_api
from .auth import (
    get_connection_credentials,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    QuotaExceededError,
    ValidationError,
    GoogleDocsAPIError
)

def register_tools(mcp: FastMCP):
    """Register all Google Docs tools with the MCP server."""

    @mcp.tool()
    def get_document(document_id: str) -> DocumentResponse:
        """
        Gets the latest version of the specified Google Docs document.
        
        Args:
            document_id: The ID of the document to retrieve
            
        Returns:
            DocumentResponse with document data
            
        Raises:
            ValidationError: If document_id is invalid
            AuthenticationError: If authentication fails
            AuthorizationError: If access is denied
            ResourceNotFoundError: If document is not found
            GoogleDocsAPIError: For other API errors
        """
        result = get_document_api(document_id)
        
        return DocumentResponse(
            documentId=result.get("documentId", document_id),
            title=result.get("title", ""),
            body=result.get("body"),
            revisionId=result.get("revisionId"),
            suggestionsViewMode=result.get("suggestionsViewMode"),
            namedRanges=result.get("namedRanges"),
            lists=result.get("lists"),
            documentStyle=result.get("documentStyle"),
            footers=result.get("footers"),
            headers=result.get("headers"),
            footnotes=result.get("footnotes"),
            inlineObjects=result.get("inlineObjects"),
            positionedObjects=result.get("positionedObjects")
        )

    @mcp.tool()
    def create_document(title: str = "Untitled document") -> CreateDocumentResponse:
        """
        Creates a blank Google Docs document using the title given in the request.
        
        Args:
            title: The title for the new document (default: "Untitled document")
            
        Returns:
            CreateDocumentResponse with created document data
            
        Raises:
            ValidationError: If title is invalid
            AuthenticationError: If authentication fails
            AuthorizationError: If access is denied
            GoogleDocsAPIError: For other API errors
        """
        result = create_document_api(title)
        
        return CreateDocumentResponse(
            documentId=result.get("documentId", ""),
            title=result.get("title", title),
            revisionId=result.get("revisionId", ""),
            body=result.get("body")
        )

    @mcp.tool()
    def batch_update_document(
        document_id: str, 
        requests_data: List[Dict[str, Any]],
        write_control: Optional[Dict[str, Any]] = None
    ) -> BatchUpdateResponse:
        """
        Applies one or more updates to the Google Docs document.
        
        Args:
            document_id: The ID of the document to update
            requests_data: List of update requests to apply to the document
            write_control: Optional write control settings
            
        Returns:
            BatchUpdateResponse with update results
            
        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            AuthorizationError: If access is denied
            ResourceNotFoundError: If document is not found
            GoogleDocsAPIError: For other API errors
        """
        result = batch_update_document_api(document_id, requests_data, write_control)
        
        return BatchUpdateResponse(
            documentId=document_id,
            writeControl=result.get("writeControl"),
            replies=result.get("replies")
        )

    @mcp.tool()
    def insert_text(
        document_id: str, 
        text: str, 
        index: int = 1
    ) -> BatchUpdateResponse:
        """
        Inserts text at the specified index in the Google Docs document.
        
        Args:
            document_id: The ID of the document to update
            text: The text to insert
            index: The index where to insert the text (default: 1, which is at the beginning)
            
        Returns:
            BatchUpdateResponse with update results
            
        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            AuthorizationError: If access is denied
            ResourceNotFoundError: If document is not found
            GoogleDocsAPIError: For other API errors
        """
        if not text:
            raise ValidationError("Text to insert cannot be empty")
            
        if index < 1:
            raise ValidationError("Index must be greater than 0")
        
        requests_data = [
            {
                "insertText": {
                    "location": {
                        "index": index
                    },
                    "text": text
                }
            }
        ]
        
        return batch_update_document(document_id, requests_data)

    @mcp.tool()
    def replace_all_text(
        document_id: str, 
        find_text: str, 
        replace_text: str,
        match_case: bool = False
    ) -> BatchUpdateResponse:
        """
        Replaces all instances of text in the Google Docs document.
        
        Args:
            document_id: The ID of the document to update
            find_text: The text to find and replace
            replace_text: The text to replace with
            match_case: Whether to match case when finding text (default: False)
            
        Returns:
            BatchUpdateResponse with update results
            
        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            AuthorizationError: If access is denied
            ResourceNotFoundError: If document is not found
            GoogleDocsAPIError: For other API errors
        """
        if not find_text:
            raise ValidationError("Find text cannot be empty")
        
        requests_data = [
            {
                "replaceAllText": {
                    "containsText": {
                        "text": find_text,
                        "matchCase": match_case
                    },
                    "replaceText": replace_text
                }
            }
        ]
        
        return batch_update_document(document_id, requests_data)

    @mcp.tool()
    def delete_content_range(
        document_id: str, 
        start_index: int, 
        end_index: int
    ) -> BatchUpdateResponse:
        """
        Deletes content in the specified range from the Google Docs document.
        
        Args:
            document_id: The ID of the document to update
            start_index: The start index of the range to delete
            end_index: The end index of the range to delete
            
        Returns:
            BatchUpdateResponse with update results
            
        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            AuthorizationError: If access is denied
            ResourceNotFoundError: If document is not found
            GoogleDocsAPIError: For other API errors
        """
        if start_index < 1:
            raise ValidationError("Start index must be greater than 0")
            
        if end_index <= start_index:
            raise ValidationError(f"End index ({end_index}) must be greater than start index ({start_index})")
        
        requests_data = [
            {
                "deleteContentRange": {
                    "range": {
                        "startIndex": start_index,
                        "endIndex": end_index
                    }
                }
            }
        ]
        
        return batch_update_document(document_id, requests_data)
