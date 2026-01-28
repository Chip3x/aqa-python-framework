import allure
import pytest

from config import settings
from src.ui.pages.dashboard_page import DashboardPage
from src.ui.pages.login_page import LoginPage


@allure.epic("UI")
@allure.feature("Authentication")
@pytest.mark.ui
class TestLogin:
    """Login page UI tests."""

    @allure.story("Login")
    @allure.title("Login page loads correctly")
    @pytest.mark.smoke
    def test_login_page_loads(self, login_page: LoginPage) -> None:
        """Test that login page loads with all elements."""
        login_page.open()

        login_page.assert_login_page_loaded()

    @allure.story("Login")
    @allure.title("Successful login with valid credentials")
    @pytest.mark.smoke
    def test_login_with_valid_credentials(
        self,
        login_page: LoginPage,
        dashboard_page: DashboardPage,
    ) -> None:
        """Test successful login redirects to dashboard."""
        login_page.open()
        login_page.login(
            email=settings.test_user_email,
            password=settings.test_user_password.get_secret_value(),
        )

        dashboard_page.assert_url_contains("/dashboard")
        dashboard_page.assert_dashboard_loaded()

    @allure.story("Login")
    @allure.title("Login with invalid credentials shows error")
    def test_login_with_invalid_credentials(self, login_page: LoginPage) -> None:
        """Test login with wrong password shows error message."""
        login_page.open()
        login_page.login(
            email=settings.test_user_email,
            password="wrong_password",
        )

        assert login_page.is_error_displayed()

    @allure.story("Login")
    @allure.title("Login with empty email shows validation")
    def test_login_with_empty_email(self, login_page: LoginPage) -> None:
        """Test login with empty email shows validation error."""
        login_page.open()
        login_page.enter_password("password123")
        login_page.click_login_button()

        assert login_page.is_error_displayed()

    @allure.story("Login")
    @allure.title("Login with empty password shows validation")
    def test_login_with_empty_password(self, login_page: LoginPage) -> None:
        """Test login with empty password shows validation error."""
        login_page.open()
        login_page.enter_email("test@example.com")
        login_page.click_login_button()

        assert login_page.is_error_displayed()

    @allure.story("Navigation")
    @allure.title("Forgot password link navigates correctly")
    def test_forgot_password_navigation(self, login_page: LoginPage) -> None:
        """Test forgot password link navigation."""
        login_page.open()
        login_page.click_forgot_password()

        login_page.assert_url_contains("/forgot-password")
