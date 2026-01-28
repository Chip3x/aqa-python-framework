import allure
import httpx
import pydantic
import pytest

from config import settings
from src.api.endpoints.auth import AuthAPI
from src.utils.auth_helper import AuthHelper


@allure.epic("API")
@allure.feature("Authentication")
@pytest.mark.api
class TestAuth:
    """Authentication API tests."""

    @allure.story("Login")
    @allure.title("Login with valid credentials")
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, auth_helper: AuthHelper) -> None:
        """Test successful login with valid credentials."""
        token = auth_helper.login_as_test_user()

        assert token is not None
        assert len(token) > 0

    @allure.story("Login")
    @allure.title("Login with invalid password")
    def test_login_with_invalid_password(self, unauthenticated_auth_api: AuthAPI) -> None:
        """Test login failure with invalid password."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            unauthenticated_auth_api.login(
                email=settings.test_user_email,
                password="wrong_password",
            )

        assert exc_info.value.response.status_code == 401

    @allure.story("Login")
    @allure.title("Login with invalid email format")
    def test_login_with_invalid_email_format(self, unauthenticated_auth_api: AuthAPI) -> None:
        """Test login failure with invalid email format."""
        with pytest.raises(pydantic.ValidationError):
            unauthenticated_auth_api.login(
                email="invalid-email",
                password="password123",
            )

    @allure.story("Token")
    @allure.title("Refresh access token")
    def test_refresh_token(self, auth_helper: AuthHelper) -> None:
        """Test token refresh functionality."""
        # First login to get tokens
        auth_helper.login_as_test_user()

        # Refresh token
        new_token = auth_helper.refresh_access_token()

        assert new_token is not None
        assert len(new_token) > 0

    @allure.story("Logout")
    @allure.title("Logout clears token")
    def test_logout_clears_token(self, auth_helper: AuthHelper) -> None:
        """Test that logout clears the authentication token."""
        auth_helper.login_as_test_user()
        assert auth_helper.token is not None

        auth_helper.logout()

        assert auth_helper.token is None
