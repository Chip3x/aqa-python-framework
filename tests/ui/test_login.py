import allure
import pytest

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
