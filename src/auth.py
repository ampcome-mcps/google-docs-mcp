"""Authentication utilities for Google Docs MCP Server."""

import os
from typing import Any, Dict
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Custom exceptions for better error handling
class GoogleDocsAPIError(Exception):
    """Base exception for Google Docs API errors"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)

class AuthenticationError(GoogleDocsAPIError):
    """Raised when authentication fails"""
    pass

class AuthorizationError(GoogleDocsAPIError):
    """Raised when user lacks permission for the operation"""
    pass

class ResourceNotFoundError(GoogleDocsAPIError):
    """Raised when requested resource is not found"""
    pass

class QuotaExceededError(GoogleDocsAPIError):
    """Raised when API quota is exceeded"""
    pass

class ValidationError(GoogleDocsAPIError):
    """Raised when request validation fails"""
    pass

# Global variable to cache access token
_cached_access_token = None

def get_connection_credentials() -> dict[str, Any]:
    """Get credentials from Nango"""
    # Validate required environment variables
    required_vars = ["NANGO_CONNECTION_ID", "NANGO_INTEGRATION_ID", "NANGO_BASE_URL", "NANGO_SECRET_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        raise AuthenticationError(f"Missing required environment variables: {', '.join(missing_vars)}")

    id = os.environ.get("NANGO_CONNECTION_ID")
    integration_id = os.environ.get("NANGO_INTEGRATION_ID")
    base_url = os.environ.get("NANGO_BASE_URL")
    secret_key = os.environ.get("NANGO_SECRET_KEY")
    
    url = f"{base_url}/connection/{id}"
    params = {
        "provider_config_key": integration_id,
        "refresh_token": "true",
    }
    headers = {"Authorization": f"Bearer {secret_key}"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise AuthenticationError("Timeout while connecting to Nango authentication service")
    except requests.exceptions.ConnectionError:
        raise AuthenticationError("Failed to connect to Nango authentication service")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise AuthenticationError("Invalid Nango secret key")
        elif response.status_code == 404:
            raise AuthenticationError("Nango connection not found")
        else:
            raise AuthenticationError(f"Nango API error: {response.status_code} - {response.text}")
    except Exception as e:
        raise AuthenticationError(f"Unexpected error getting Nango credentials: {str(e)}")

def get_access_token() -> str:
    """Get access token from Nango, with caching"""
    global _cached_access_token
    
    if _cached_access_token is None:
        credentials = get_connection_credentials()
        _cached_access_token = credentials.get("credentials", {}).get("access_token")
        
        if not _cached_access_token:
            raise AuthenticationError("No access token found in Nango credentials")
    
    return _cached_access_token

def refresh_access_token() -> str:
    """Force refresh access token from Nango"""
    global _cached_access_token
    _cached_access_token = None
    return get_access_token()

def get_auth_headers() -> Dict[str, str]:
    """Get authentication headers for Google API requests using Nango"""
    access_token = get_access_token()
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
