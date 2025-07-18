"""API client utilities for Google Docs MCP Server."""

from typing import Any, Dict
import requests

from .auth import get_auth_headers

# Base URL for Google Docs API
BASE_URL = "https://docs.googleapis.com"


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


def get_document_api(document_id: str) -> Dict[str, Any]:
    """Get document from Google Docs API."""
    url = f"{BASE_URL}/v1/documents/{document_id}"
    return make_request("GET", url)


def create_document_api(title: str) -> Dict[str, Any]:
    """Create document via Google Docs API."""
    url = f"{BASE_URL}/v1/documents"
    payload = {"title": title}
    return make_request("POST", url, json=payload)


def batch_update_document_api(document_id: str, requests_data: list, write_control: dict = None) -> Dict[str, Any]:
    """Batch update document via Google Docs API."""
    url = f"{BASE_URL}/v1/documents/{document_id}:batchUpdate"
    payload = {"requests": requests_data}
    
    if write_control:
        payload["writeControl"] = write_control
    
    return make_request("POST", url, json=payload)
