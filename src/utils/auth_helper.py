from typing import cast

import allure

from config.settings import Settings
from src.api.client import APIClient
from src.api.endpoints.auth import AuthAPI
from src.utils.logger import logger


class AuthHelper:
    """Helper class for authentication operations."""

    def __init__(self, settings: Settings, api_client: APIClient | None = None) -> None:
        """Initialize auth helper.

        Args:
            settings: Settings instance.
            api_client: Optional API client. Creates new one if not provided.
        """
        self._settings = settings
        self._client = api_client or APIClient(settings=settings)
        self._auth_api = AuthAPI(self._client, settings)
        self._token: str | None = None

    @property
    def token(self) -> str | None:
        """Get current access token."""
        return self._token

    @property
    def client(self) -> APIClient:
        """Get authenticated API client."""
        return self._client

    @allure.step("Authenticate with test user credentials")
    def login_as_test_user(self) -> str:
        """Login using test user credentials from settings.

        Returns:
            Access token.
        """
        email = self._settings.test_user_email
        password = self._settings.test_user_password.get_secret_value()
        return str(self.login(email, password))

    @allure.step("Authenticate with email: {email}")
    def login(self, email: str, password: str) -> str:
        """Login with provided credentials.

        Args:
            email: User email.
            password: User password.

        Returns:
            Access token.
        """
        logger.info(f"Authenticating user: {email}")
        token = cast(str, self._auth_api.login(email, password))
        self._token = token
        self._client.set_token(token)
        logger.info("Authentication successful")
        return token

    @allure.step("Logout")
    def logout(self) -> None:
        """Clear token locally."""
        logger.info("Clearing auth token")
        self._client.clear_token()
        self._token = None
        logger.info("Auth token cleared")
