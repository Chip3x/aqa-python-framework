from typing import Any

import allure
import httpx

from config import settings
from src.utils.logger import logger


class APIClient:
    """Base HTTP client for API testing."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize API client.

        Args:
            base_url: Base URL for API requests. Defaults to settings.api_url.
            timeout: Request timeout in seconds. Defaults to settings.api_timeout_seconds.
            headers: Default headers for all requests.
        """
        self.base_url = base_url or settings.api_url
        self.timeout = timeout or settings.api_timeout_seconds
        self._default_headers = headers or {}
        self._token: str | None = None
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        """Get or create HTTP client instance."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._default_headers,
            )
        return self._client

    def set_token(self, token: str) -> None:
        """Set authorization token for subsequent requests.

        Args:
            token: JWT or OAuth token.
        """
        self._token = token
        logger.debug(f"Token set: {token[:20]}...")

    def clear_token(self) -> None:
        """Clear authorization token."""
        self._token = None
        logger.debug("Token cleared")

    def _get_headers(self, headers: dict[str, str] | None = None) -> dict[str, str]:
        """Merge default headers with request-specific headers.

        Args:
            headers: Request-specific headers.

        Returns:
            Merged headers dictionary.
        """
        result = self._default_headers.copy()
        if self._token:
            result["Authorization"] = f"Bearer {self._token}"
        if headers:
            result.update(headers)
        return result

    def _log_request(self, method: str, url: str, **kwargs: Any) -> None:
        """Log request details."""
        logger.info(f"Request: {method} {url}")
        if kwargs.get("json"):
            logger.debug(f"Body: {kwargs['json']}")
        if kwargs.get("params"):
            logger.debug(f"Params: {kwargs['params']}")

    def _log_response(self, response: httpx.Response) -> None:
        """Log response details."""
        logger.info(f"Response: {response.status_code} {response.reason_phrase}")
        logger.debug(f"Response body: {response.text[:500]}")

    @allure.step("GET {url}")
    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send GET request.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            headers: Additional headers.

        Returns:
            HTTP response.
        """
        self._log_request("GET", url, params=params)
        response = self.client.get(url, params=params, headers=self._get_headers(headers))
        self._log_response(response)
        return response

    @allure.step("POST {url}")
    def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send POST request.

        Args:
            url: Request URL (relative to base_url).
            json: JSON body.
            data: Form data.
            headers: Additional headers.

        Returns:
            HTTP response.
        """
        self._log_request("POST", url, json=json, data=data)
        response = self.client.post(url, json=json, data=data, headers=self._get_headers(headers))
        self._log_response(response)
        return response

    @allure.step("PUT {url}")
    def put(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send PUT request.

        Args:
            url: Request URL (relative to base_url).
            json: JSON body.
            headers: Additional headers.

        Returns:
            HTTP response.
        """
        self._log_request("PUT", url, json=json)
        response = self.client.put(url, json=json, headers=self._get_headers(headers))
        self._log_response(response)
        return response

    @allure.step("PATCH {url}")
    def patch(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send PATCH request.

        Args:
            url: Request URL (relative to base_url).
            json: JSON body.
            headers: Additional headers.

        Returns:
            HTTP response.
        """
        self._log_request("PATCH", url, json=json)
        response = self.client.patch(url, json=json, headers=self._get_headers(headers))
        self._log_response(response)
        return response

    @allure.step("DELETE {url}")
    def delete(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send DELETE request.

        Args:
            url: Request URL (relative to base_url).
            headers: Additional headers.

        Returns:
            HTTP response.
        """
        self._log_request("DELETE", url)
        response = self.client.delete(url, headers=self._get_headers(headers))
        self._log_response(response)
        return response

    def close(self) -> None:
        """Close HTTP client."""
        if self._client and not self._client.is_closed:
            self._client.close()
            logger.debug("API client closed")

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
