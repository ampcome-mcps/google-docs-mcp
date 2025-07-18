#!/usr/bin/env python3
"""Google Docs MCP Server with structured output."""

import json
import os
from typing import Any, Dict, List, Optional
import requests
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize FastMCP server
mcp = FastMCP("Google Docs API")

# Base URL for Google Docs API
BASE_URL = "https://docs.googleapis.com"

# Structured output models

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



class ErrorResponse(BaseModel):
    """Error response structure."""
    error: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
    details: Optional[str] = Field(default=None, description="Additional error details")



def get_connection_credentials() -> dict[str, Any]:
    """Get credentials from Nango"""
    id = os.environ.get("NANGO_CONNECTION_ID")
    integration_id = os.environ.get("NANGO_INTEGRATION_ID")
    base_url = os.environ.get("NANGO_BASE_URL")
    secret_key = os.environ.get("NANGO_SECRET_KEY")
    
    if not all([id, integration_id, base_url, secret_key]):
        raise ValueError("All Nango environment variables are required: NANGO_CONNECTION_ID, NANGO_INTEGRATION_ID, NANGO_BASE_URL, NANGO_SECRET_KEY")
    
    url = f"{base_url}/connection/{id}"
    params = {
        "provider_config_key": integration_id,
        "refresh_token": "true",
    }
    headers = {"Authorization": f"Bearer {secret_key}"}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for bad status codes
    
    return response.json()


def get_auth_headers() -> Dict[str, str]:
    """Get authentication headers for Google API requests using Nango."""
    try:
        credentials = get_connection_credentials()
        access_token = credentials.get("credentials", {}).get("access_token")
        
        if not access_token:
            raise ValueError("No access token found in Nango credentials")
        
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    except Exception as e:
        raise ValueError(f"Failed to get credentials from Nango: {str(e)}")


def make_request(method: str, url: str, **kwargs) -> Dict[str, Any]:
    """Make an authenticated request to the Google Docs API."""
    try:
        headers = get_auth_headers()
        response = requests.request(method, url, headers=headers, **kwargs)
        
        if response.status_code >= 400:
            return {
                "error": f"API request failed: {response.reason}",
                "status_code": response.status_code,
                "details": response.text
            }
        
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}",
            "status_code": 500,
            "details": None
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "status_code": 500,
            "details": None
        }


@mcp.tool()
def get_document(document_id: str) -> DocumentResponse | ErrorResponse:
    """
    Gets the latest version of the specified Google Docs document.
    
    Args:
        document_id: The ID of the document to retrieve
        
    Returns:
        DocumentResponse with document data or ErrorResponse if failed
    """
    url = f"{BASE_URL}/v1/documents/{document_id}"
    result = make_request("GET", url)
    
    if "error" in result:
        return ErrorResponse(**result)
    
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
def create_document(title: str = "Untitled document") -> CreateDocumentResponse | ErrorResponse:
    """
    Creates a blank Google Docs document using the title given in the request.
    
    Args:
        title: The title for the new document (default: "Untitled document")
        
    Returns:
        CreateDocumentResponse with created document data or ErrorResponse if failed
    """
    url = f"{BASE_URL}/v1/documents"
    payload = {
        "title": title
    }
    
    result = make_request("POST", url, json=payload)
    
    if "error" in result:
        return ErrorResponse(**result)
    
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
) -> BatchUpdateResponse | ErrorResponse:
    """
    Applies one or more updates to the Google Docs document.
    
    Args:
        document_id: The ID of the document to update
        requests_data: List of update requests to apply to the document
        write_control: Optional write control settings
        
    Returns:
        BatchUpdateResponse with update results or ErrorResponse if failed
    """
    url = f"{BASE_URL}/v1/documents/{document_id}:batchUpdate"
    payload = {
        "requests": requests_data
    }
    
    if write_control:
        payload["writeControl"] = write_control
    
    result = make_request("POST", url, json=payload)
    
    if "error" in result:
        return ErrorResponse(**result)
    
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
) -> BatchUpdateResponse | ErrorResponse:
    """
    Inserts text at the specified index in the Google Docs document.
    
    Args:
        document_id: The ID of the document to update
        text: The text to insert
        index: The index where to insert the text (default: 1, which is at the beginning)
        
    Returns:
        BatchUpdateResponse with update results or ErrorResponse if failed
    """
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
) -> BatchUpdateResponse | ErrorResponse:
    """
    Replaces all instances of text in the Google Docs document.
    
    Args:
        document_id: The ID of the document to update
        find_text: The text to find and replace
        replace_text: The text to replace with
        match_case: Whether to match case when finding text (default: False)
        
    Returns:
        BatchUpdateResponse with update results or ErrorResponse if failed
    """
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
) -> BatchUpdateResponse | ErrorResponse:
    """
    Deletes content in the specified range from the Google Docs document.
    
    Args:
        document_id: The ID of the document to update
        start_index: The start index of the range to delete
        end_index: The end index of the range to delete
        
    Returns:
        BatchUpdateResponse with update results or ErrorResponse if failed
    """
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


if __name__ == "__main__":
    # Run the server using stdio transport
    mcp.run()