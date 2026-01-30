from typing import cast

from src.api.client import APIClient
from src.api.contracts.registry import ContractRegistry


class HealthService:
    """Health check service with contract validation."""

    def __init__(self, client: APIClient, contracts: ContractRegistry) -> None:
        self._client = client
        self._contracts = contracts

    def public_health(self) -> str:
        response = self._client.get("/api/public/health")
        response.raise_for_status()
        body = cast(str, response.text).strip()
        self._contracts.validate("GET", "/api/public/health", body)
        return body

    def secured_health(self, token: str) -> str:
        self._client.set_token(token)
        try:
            response = self._client.get("/api/secured/health")
            response.raise_for_status()
            body = cast(str, response.text).strip()
            self._contracts.validate("GET", "/api/secured/health", body)
            return body
        finally:
            self._client.clear_token()
