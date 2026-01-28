import allure
from playwright.sync_api import Page


class Sidebar:
    """Sidebar navigation component."""

    # Selectors
    SIDEBAR_CONTAINER = "[data-testid='sidebar']"
    MENU_ITEM = "[data-testid='menu-item-{name}']"
    COLLAPSE_BUTTON = "[data-testid='sidebar-collapse']"
    ACTIVE_ITEM = "[data-testid='sidebar'] .active"

    def __init__(self, page: Page) -> None:
        """Initialize sidebar component.

        Args:
            page: Playwright page instance.
        """
        self.page = page

    @allure.step("Navigate to menu item: {name}")
    def navigate_to(self, name: str) -> None:
        """Click menu item by name.

        Args:
            name: Menu item identifier.
        """
        selector = self.MENU_ITEM.format(name=name)
        self.page.click(selector)

    @allure.step("Toggle sidebar")
    def toggle(self) -> None:
        """Toggle sidebar collapse/expand."""
        self.page.click(self.COLLAPSE_BUTTON)

    def is_collapsed(self) -> bool:
        """Check if sidebar is collapsed.

        Returns:
            True if sidebar is in collapsed state.
        """
        sidebar = self.page.locator(self.SIDEBAR_CONTAINER)
        return "collapsed" in (sidebar.get_attribute("class") or "")

    def get_active_menu_item(self) -> str:
        """Get currently active menu item text.

        Returns:
            Active menu item text.
        """
        return str(self.page.inner_text(self.ACTIVE_ITEM))

    def is_visible(self) -> bool:
        """Check if sidebar is visible.

        Returns:
            True if sidebar is visible.
        """
        return bool(self.page.is_visible(self.SIDEBAR_CONTAINER))
