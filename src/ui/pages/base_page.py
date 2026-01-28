from typing import Literal, TypeVar

import allure
from playwright.sync_api import Page, expect

from config import settings
from src.utils.logger import logger

T = TypeVar("T", bound="BasePage")


class BasePage:
    """Base page object with common methods."""

    url_path: str = ""

    def __init__(self, page: Page) -> None:
        """Initialize base page.

        Args:
            page: Playwright page instance.
        """
        self.page = page
        self.base_url = settings.base_url

    @property
    def url(self) -> str:
        """Get full page URL."""
        return f"{self.base_url}{self.url_path}"

    @allure.step("Open page: {0.url}")
    def open(self: T) -> T:
        """Open page by URL.

        Returns:
            Self for chaining.
        """
        logger.info(f"Opening page: {self.url}")
        self.page.goto(self.url)
        return self

    @allure.step("Wait for page load")
    def wait_for_load(self: T) -> T:
        """Wait for page to fully load.

        Returns:
            Self for chaining.
        """
        self.page.wait_for_load_state("networkidle")
        return self

    @allure.step("Get page title")
    def get_title(self) -> str:
        """Get page title.

        Returns:
            Page title string.
        """
        return str(self.page.title())

    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        """Get current page URL.

        Returns:
            Current URL string.
        """
        return str(self.page.url)

    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Take screenshot of current page.

        Args:
            name: Screenshot name for Allure report.

        Returns:
            Screenshot bytes.
        """
        screenshot: bytes = self.page.screenshot()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot

    @allure.step("Click element: {selector}")
    def click(self, selector: str) -> None:
        """Click element by selector.

        Args:
            selector: Element selector.
        """
        logger.debug(f"Clicking element: {selector}")
        self.page.click(selector)

    @allure.step("Fill input: {selector}")
    def fill(self, selector: str, value: str) -> None:
        """Fill input field with value.

        Args:
            selector: Input selector.
            value: Value to fill.
        """
        logger.debug(f"Filling {selector} with value")
        self.page.fill(selector, value)

    @allure.step("Get text from: {selector}")
    def get_text(self, selector: str) -> str:
        """Get text content of element.

        Args:
            selector: Element selector.

        Returns:
            Element text content.
        """
        return str(self.page.inner_text(selector))

    @allure.step("Check element is visible: {selector}")
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible.

        Args:
            selector: Element selector.

        Returns:
            True if element is visible.
        """
        return bool(self.page.is_visible(selector))

    @allure.step("Wait for element: {selector}")
    def wait_for_element(
        self,
        selector: str,
        state: Literal["attached", "detached", "hidden", "visible"] = "visible",
    ) -> None:
        """Wait for element to reach specified state.

        Args:
            selector: Element selector.
            state: Expected state (visible, hidden, attached, detached).
        """
        logger.debug(f"Waiting for {selector} to be {state}")
        self.page.wait_for_selector(selector, state=state)

    @allure.step("Assert element is visible: {selector}")
    def assert_element_visible(self, selector: str) -> None:
        """Assert element is visible.

        Args:
            selector: Element selector.
        """
        expect(self.page.locator(selector)).to_be_visible()

    @allure.step("Assert element has text: {text}")
    def assert_element_has_text(self, selector: str, text: str) -> None:
        """Assert element contains text.

        Args:
            selector: Element selector.
            text: Expected text.
        """
        expect(self.page.locator(selector)).to_contain_text(text)

    @allure.step("Assert URL contains: {url_part}")
    def assert_url_contains(self, url_part: str) -> None:
        """Assert current URL contains string.

        Args:
            url_part: Expected URL part.
        """
        expect(self.page).to_have_url(f"*{url_part}*")
