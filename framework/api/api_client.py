"""API Client for making HTTP requests"""
import requests
from typing import Dict, Any, Optional, Union
import json
from framework.config.settings import settings


class APIClient:
    """
    API Client for making HTTP requests.
    Supports GET, POST, PUT, DELETE, PATCH methods.
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.API_BASE_URL
        self.session = requests.Session()
        self.timeout = settings.TIMEOUT // 1000  # Convert to seconds
        self.headers = {}
    
    def set_header(self, key: str, value: str) -> None:
        """Set a header"""
        self.headers[key] = value
        self.session.headers.update({key: value})
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        """Set multiple headers"""
        self.headers.update(headers)
        self.session.headers.update(headers)
    
    def set_auth(self, username: str, password: str) -> None:
        """Set basic authentication"""
        self.session.auth = (username, password)
    
    def set_bearer_token(self, token: str) -> None:
        """Set bearer token"""
        self.set_header("Authorization", f"Bearer {token}")
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make GET request"""
        url = self._build_url(endpoint)
        return self.session.get(url, params=params, timeout=self.timeout, **kwargs)
    
    def post(self, 
             endpoint: str, 
             data: Optional[Dict] = None, 
             json: Optional[Dict] = None,
             **kwargs) -> requests.Response:
        """Make POST request"""
        url = self._build_url(endpoint)
        return self.session.post(url, data=data, json=json, timeout=self.timeout, **kwargs)
    
    def put(self, 
            endpoint: str, 
            data: Optional[Dict] = None, 
            json: Optional[Dict] = None,
            **kwargs) -> requests.Response:
        """Make PUT request"""
        url = self._build_url(endpoint)
        return self.session.put(url, data=data, json=json, timeout=self.timeout, **kwargs)
    
    def patch(self, 
              endpoint: str, 
              data: Optional[Dict] = None, 
              json: Optional[Dict] = None,
              **kwargs) -> requests.Response:
        """Make PATCH request"""
        url = self._build_url(endpoint)
        return self.session.patch(url, data=data, json=json, timeout=self.timeout, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request"""
        url = self._build_url(endpoint)
        return self.session.delete(url, timeout=self.timeout, **kwargs)
    
    def head(self, endpoint: str, **kwargs) -> requests.Response:
        """Make HEAD request"""
        url = self._build_url(endpoint)
        return self.session.head(url, timeout=self.timeout, **kwargs)
    
    def close(self) -> None:
        """Close session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
