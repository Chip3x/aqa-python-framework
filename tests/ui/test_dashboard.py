import allure
import pytest

from src.ui.components.header import Header
from src.ui.components.sidebar import Sidebar
from src.ui.pages.dashboard_page import DashboardPage


@allure.epic("UI")
@allure.feature("Dashboard")
@pytest.mark.ui
class TestDashboard:
    """Dashboard page UI tests."""

    @allure.story("Dashboard")
    @allure.title("Dashboard loads after login")
    @pytest.mark.smoke
    def test_dashboard_loads_after_login(
        self,
        logged_in_dashboard: DashboardPage,
    ) -> None:
        """Test dashboard page loads correctly after login."""
        logged_in_dashboard.assert_dashboard_loaded()

    @allure.story("Dashboard")
    @allure.title("Sidebar is visible on dashboard")
    def test_sidebar_visible(
        self,
        logged_in_dashboard: DashboardPage,
        sidebar: Sidebar,
    ) -> None:
        """Test sidebar component is visible."""
        assert logged_in_dashboard.is_sidebar_visible()
        assert sidebar.is_visible()

    @allure.story("Navigation")
    @allure.title("User can logout from dashboard")
    def test_logout_from_dashboard(
        self,
        logged_in_dashboard: DashboardPage,
    ) -> None:
        """Test user can logout and is redirected to login."""
        logged_in_dashboard.logout()

        logged_in_dashboard.assert_url_contains("/login")

    @allure.story("Header")
    @allure.title("Header shows logged in user")
    def test_header_shows_user(
        self,
        logged_in_dashboard: DashboardPage,
        header: Header,
    ) -> None:
        """Test header shows that user is logged in."""
        assert header.is_user_logged_in()

    @allure.story("Navigation")
    @allure.title("Navigate to settings")
    def test_navigate_to_settings(
        self,
        logged_in_dashboard: DashboardPage,
    ) -> None:
        """Test navigation to settings page."""
        logged_in_dashboard.go_to_settings()

        logged_in_dashboard.assert_url_contains("/settings")

    @allure.story("Sidebar")
    @allure.title("Sidebar can be collapsed")
    def test_sidebar_collapse(
        self,
        logged_in_dashboard: DashboardPage,
        sidebar: Sidebar,
    ) -> None:
        """Test sidebar collapse functionality."""
        initial_state = sidebar.is_collapsed()

        sidebar.toggle()

        assert sidebar.is_collapsed() != initial_state
