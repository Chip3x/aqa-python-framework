import allure

from config import settings
from src.api.client import APIClient
from src.api.endpoints.auth import AuthAPI
from src.utils.logger import logger


class AuthHelper:
    """Helper class for authentication operations."""

    def __init__(self, api_client: APIClient | None = None) -> None:
        """Initialize auth helper.

        Args:
            api_client: Optional API client. Creates new one if not provided.
        """
        self._client = api_client or APIClient()
        self._auth_api = AuthAPI(self._client)
        self._token: str | None = None
        self._refresh_token: str | None = None

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
        email = settings.test_user_email
        password = settings.test_user_password.get_secret_value()
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
        response = self._auth_api.login(email, password)
        token: str = response.access_token
        self._token = token
        self._refresh_token = response.refresh_token
        self._client.set_token(token)
        logger.info("Authentication successful")
        return token

    @allure.step("Authenticate with OAuth")
    def login_with_oauth(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        scope: str | None = None,
    ) -> str:
        """Login using OAuth client credentials.

        Args:
            client_id: OAuth client ID. Defaults to settings value.
            client_secret: OAuth client secret. Defaults to settings value.
            scope: OAuth scope.

        Returns:
            Access token.
        """
        resolved_client_id = client_id or settings.oauth_client_id
        resolved_client_secret = client_secret or settings.oauth_client_secret.get_secret_value()

        logger.info(f"Authenticating with OAuth client: {resolved_client_id}")
        response = self._auth_api.get_oauth_token(resolved_client_id, resolved_client_secret, scope)
        token: str = response.access_token
        self._token = token
        self._client.set_token(token)
        logger.info("OAuth authentication successful")
        return token

    @allure.step("Refresh access token")
    def refresh_access_token(self) -> str:
        """Refresh access token using refresh token.

        Returns:
            New access token.

        Raises:
            ValueError: If no refresh token available.
        """
        if not self._refresh_token:
            raise ValueError("No refresh token available")

        logger.info("Refreshing access token")
        response = self._auth_api.refresh_token(self._refresh_token)
        token: str = response.access_token
        self._token = token
        self._refresh_token = response.refresh_token
        self._client.set_token(token)
        logger.info("Token refresh successful")
        return token

    @allure.step("Logout")
    def logout(self) -> None:
        """Logout and clear tokens."""
        logger.info("Logging out")
        self._auth_api.logout()
        self._token = None
        self._refresh_token = None
        logger.info("Logout successful")
