import allure

from src.api.client import APIClient


class AccountAPI:
    """Account profile endpoints."""

    def __init__(self, client: APIClient) -> None:
        """Initialize Account API.

        Args:
            client: API client instance.
        """
        self.client = client
        self._base_path = "/api/secured/account"

    @allure.step("Delete current user profile")
    def delete_current(self) -> None:
        """Delete current user profile."""
        response = self.client.delete(f"{self._base_path}/delete")
        response.raise_for_status()
