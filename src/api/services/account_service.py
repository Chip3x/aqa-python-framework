from src.api.client import APIClient
from src.api.contracts.registry import ContractRegistry


class AccountService:
    """Account service with contract validation."""

    def __init__(self, client: APIClient, contracts: ContractRegistry) -> None:
        self._client = client
        self._contracts = contracts

    def delete_current(self) -> None:
        response = self._client.delete("/api/secured/account/delete")
        response.raise_for_status()
        self._contracts.validate("DELETE", "/api/secured/account/delete", response.text)
