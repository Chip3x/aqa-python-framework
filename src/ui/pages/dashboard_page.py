import allure
from playwright.sync_api import Page

from src.ui.pages.base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard page object."""

    url_path = "/dashboard"

    # Selectors
    WELCOME_MESSAGE = "[data-testid='welcome-message']"
    USER_MENU = "[data-testid='user-menu']"
    LOGOUT_BUTTON = "[data-testid='logout-button']"
    SIDEBAR = "[data-testid='sidebar']"
    MAIN_CONTENT = "[data-testid='main-content']"
    NOTIFICATIONS_ICON = "[data-testid='notifications']"
    SETTINGS_LINK = "[data-testid='settings-link']"

    def __init__(self, page: Page, base_url: str) -> None:
        """Initialize dashboard page.

        Args:
            page: Playwright page instance.
            base_url: Base URL for UI tests.
        """
        super().__init__(page, base_url)

    def get_welcome_message(self) -> str:
        """Get welcome message text.

        Returns:
            Welcome message string.
        """
        return str(self.get_text(self.WELCOME_MESSAGE))

    @allure.step("Open user menu")
    def open_user_menu(self) -> "DashboardPage":
        """Open user dropdown menu.

        Returns:
            Self for chaining.
        """
        self.click(self.USER_MENU)
        return self

    @allure.step("Logout from application")
    def logout(self) -> None:
        """Logout from application via user menu."""
        self.open_user_menu()
        self.click(self.LOGOUT_BUTTON)

    @allure.step("Navigate to settings")
    def go_to_settings(self) -> None:
        """Navigate to settings page."""
        self.click(self.SETTINGS_LINK)

    @allure.step("Click notifications icon")
    def open_notifications(self) -> "DashboardPage":
        """Open notifications panel.

        Returns:
            Self for chaining.
        """
        self.click(self.NOTIFICATIONS_ICON)
        return self

    def is_sidebar_visible(self) -> bool:
        """Check if sidebar is visible.

        Returns:
            True if sidebar is visible.
        """
        return bool(self.is_visible(self.SIDEBAR))

    def assert_dashboard_loaded(self) -> None:
        """Assert dashboard page is properly loaded."""
        self.assert_element_visible(self.WELCOME_MESSAGE)
        self.assert_element_visible(self.USER_MENU)
        self.assert_element_visible(self.SIDEBAR)

    def assert_user_logged_in(self, username: str) -> None:
        """Assert user is logged in with expected username.

        Args:
            username: Expected username in welcome message.
        """
        self.assert_element_has_text(self.WELCOME_MESSAGE, username)
