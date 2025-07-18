"""API client utilities for Google Docs MCP Server."""

from typing import Any, Dict
import requests

from .auth import (
    get_access_token, 
    refresh_access_token,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    QuotaExceededError,
    ValidationError,
    GoogleDocsAPIError
)

# Base URL for Google Docs API
BASE_URL = "https://docs.googleapis.com"

def _raise_for_status(response: requests.Response) -> None:
    """Raise appropriate exception based on HTTP status code"""
    if response.ok:
        return
    
    status_code = response.status_code
    
    try:
        error_data = response.json()
        error_message = error_data.get('error', {}).get('message', response.text)
    except:
        error_message = response.text or f"HTTP {status_code} error"
    
    if status_code == 400:
        raise ValidationError(f"Bad request: {error_message}", status_code, error_data if 'error_data' in locals() else None)
    elif status_code == 401:
        raise AuthenticationError(f"Authentication failed: {error_message}", status_code, error_data if 'error_data' in locals() else None)
    elif status_code == 403:
        raise AuthorizationError(f"Permission denied: {error_message}", status_code, error_data if 'error_data' in locals() else None)
    elif status_code == 404:
        raise ResourceNotFoundError(f"Resource not found: {error_message}", status_code, error_data if 'error_data' in locals() else None)
    elif status_code == 429:
        raise QuotaExceededError(f"Quota exceeded: {error_message}", status_code, error_data if 'error_data' in locals() else None)
    elif 500 <= status_code < 600:
        raise GoogleDocsAPIError(f"Server error: {error_message}", status_code, error_data if 'error_data' in locals() else None)
    else:
        raise GoogleDocsAPIError(f"HTTP {status_code}: {error_message}", status_code, error_data if 'error_data' in locals() else None)

def make_request(
    method: str,
    endpoint: str,
    headers: Dict[str, str] = None,
    params: Dict[str, Any] = None,
    json_data: Dict[str, Any] = None,
    data: Any = None,
    retry_auth: bool = True
) -> Dict[str, Any]:
    """Make HTTP request to Google Docs API with automatic token refresh"""
    url = f"{BASE_URL}{endpoint}"
    
    # Get access token if not provided in headers
    if not headers or "Authorization" not in headers:
        access_token = get_access_token()
        if not headers:
            headers = {}
        headers["Authorization"] = f"Bearer {access_token}"
        headers["Content-Type"] = "application/json"
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_data,
            data=data,
            timeout=30
        )
        
        # If we get a 401 and retry_auth is True, try to refresh the token
        if response.status_code == 401 and retry_auth:
            access_token = refresh_access_token()
            headers["Authorization"] = f"Bearer {access_token}"
            # Retry the request with the new token
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                data=data,
                timeout=30
            )
        
        # Raise appropriate exception for non-successful responses
        _raise_for_status(response)
        
        # Parse response data
        response_data = None
        if response.content:
            try:
                response_data = response.json()
            except:
                response_data = {"content": response.text}
        
        return response_data
        
    except requests.exceptions.Timeout:
        raise GoogleDocsAPIError("Request timeout - Google Docs API did not respond in time")
    except requests.exceptions.ConnectionError:
        raise GoogleDocsAPIError("Connection error - Unable to reach Google Docs API")
    except requests.exceptions.RequestException as e:
        raise GoogleDocsAPIError(f"Request failed: {str(e)}")

def get_document_api(document_id: str) -> Dict[str, Any]:
    """Get document from Google Docs API"""
    if not document_id or not document_id.strip():
        raise ValidationError("Document ID cannot be empty")
        
    endpoint = f"/v1/documents/{document_id.strip()}"
    return make_request("GET", endpoint)

def create_document_api(title: str) -> Dict[str, Any]:
    """Create document via Google Docs API"""
    if not title or not title.strip():
        raise ValidationError("Document title cannot be empty")
        
    endpoint = "/v1/documents"
    payload = {"title": title.strip()}
    return make_request("POST", endpoint, json_data=payload)

def batch_update_document_api(document_id: str, requests_data: list, write_control: dict = None) -> Dict[str, Any]:
    """Batch update document via Google Docs API"""
    if not document_id or not document_id.strip():
        raise ValidationError("Document ID cannot be empty")
        
    if not requests_data or not isinstance(requests_data, list):
        raise ValidationError("Requests data must be a non-empty list")
    
    endpoint = f"/v1/documents/{document_id.strip()}:batchUpdate"
    payload = {"requests": requests_data}
    
    if write_control:
        payload["writeControl"] = write_control
    
    return make_request("POST", endpoint, json_data=payload)
