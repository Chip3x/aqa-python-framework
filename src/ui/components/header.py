import allure
from playwright.sync_api import Page


class Header:
    """Header component present on multiple pages."""

    # Selectors
    LOGO = "[data-testid='logo']"
    NAVIGATION = "[data-testid='navigation']"
    SEARCH_INPUT = "[data-testid='search-input']"
    USER_AVATAR = "[data-testid='user-avatar']"

    def __init__(self, page: Page) -> None:
        """Initialize header component.

        Args:
            page: Playwright page instance.
        """
        self.page = page

    @allure.step("Click logo")
    def click_logo(self) -> None:
        """Click logo to navigate to home."""
        self.page.click(self.LOGO)

    @allure.step("Search for: {query}")
    def search(self, query: str) -> None:
        """Enter search query.

        Args:
            query: Search query string.
        """
        self.page.fill(self.SEARCH_INPUT, query)
        self.page.press(self.SEARCH_INPUT, "Enter")

    @allure.step("Click user avatar")
    def click_user_avatar(self) -> None:
        """Click user avatar to open menu."""
        self.page.click(self.USER_AVATAR)

    def is_user_logged_in(self) -> bool:
        """Check if user is logged in by avatar presence.

        Returns:
            True if user avatar is visible.
        """
        return bool(self.page.is_visible(self.USER_AVATAR))
