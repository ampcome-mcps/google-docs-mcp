"""Authentication utilities for Google Docs MCP Server."""

import os
from typing import Any, Dict
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


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
