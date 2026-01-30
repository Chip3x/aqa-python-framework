from typing import Any, cast

from src.api.client import APIClient
from src.api.contracts.registry import ContractRegistry


class CoursesService:
    """Courses service with contract validation."""

    def __init__(self, client: APIClient, contracts: ContractRegistry) -> None:
        self._client = client
        self._contracts = contracts

    def get_all(self) -> dict[str, Any]:
        response = self._client.get("/api/secured/course")
        response.raise_for_status()
        payload = cast(dict[str, Any], response.json())
        self._contracts.validate("GET", "/api/secured/course", payload)
        return payload

    def get_types(self) -> dict[str, Any]:
        response = self._client.get("/api/secured/course/types")
        response.raise_for_status()
        payload = cast(dict[str, Any], response.json())
        self._contracts.validate("GET", "/api/secured/course/types", payload)
        return payload

    def get_languages(self) -> dict[str, Any]:
        response = self._client.get("/api/secured/course/languages")
        response.raise_for_status()
        payload = cast(dict[str, Any], response.json())
        self._contracts.validate("GET", "/api/secured/course/languages", payload)
        return payload

    def get_countries(self) -> dict[str, Any]:
        response = self._client.get("/api/secured/course/countries")
        response.raise_for_status()
        payload = cast(dict[str, Any], response.json())
        self._contracts.validate("GET", "/api/secured/course/countries", payload)
        return payload
