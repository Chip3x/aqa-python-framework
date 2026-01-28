import allure

from src.api.client import APIClient
from src.api.models.auth import (
    LoginRequest,
    LoginResponse,
    OAuthTokenRequest,
    OAuthTokenResponse,
    TokenRefreshRequest,
)


class AuthAPI:
    """Authentication API endpoints."""

    def __init__(self, client: APIClient) -> None:
        """Initialize Auth API.

        Args:
            client: API client instance.
        """
        self.client = client
        self._base_path = "/auth"

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str) -> LoginResponse:
        """Authenticate user with email and password.

        Args:
            email: User email.
            password: User password.

        Returns:
            Login response with tokens.
        """
        request = LoginRequest(email=email, password=password)
        response = self.client.post(f"{self._base_path}/login", json=request.model_dump())
        response.raise_for_status()
        return LoginResponse.model_validate(response.json())

    @allure.step("Refresh access token")
    def refresh_token(self, refresh_token: str) -> LoginResponse:
        """Refresh access token using refresh token.

        Args:
            refresh_token: Valid refresh token.

        Returns:
            New login response with tokens.
        """
        request = TokenRefreshRequest(refresh_token=refresh_token)
        response = self.client.post(f"{self._base_path}/refresh", json=request.model_dump())
        response.raise_for_status()
        return LoginResponse.model_validate(response.json())

    @allure.step("Get OAuth token")
    def get_oauth_token(
        self,
        client_id: str,
        client_secret: str,
        scope: str | None = None,
    ) -> OAuthTokenResponse:
        """Get OAuth access token using client credentials.

        Args:
            client_id: OAuth client ID.
            client_secret: OAuth client secret.
            scope: Optional OAuth scope.

        Returns:
            OAuth token response.
        """
        request = OAuthTokenRequest(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
        )
        response = self.client.post(
            f"{self._base_path}/oauth/token",
            data=request.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return OAuthTokenResponse.model_validate(response.json())

    @allure.step("Logout")
    def logout(self) -> None:
        """Logout current user and invalidate tokens."""
        response = self.client.post(f"{self._base_path}/logout")
        response.raise_for_status()
        self.client.clear_token()
