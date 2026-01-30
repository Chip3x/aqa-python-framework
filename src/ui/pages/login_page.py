import allure
from playwright.sync_api import Page

from src.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object."""

    url_path = "/login"

    # Selectors
    EMAIL_INPUT = "//input[@name='email']"
    PASSWORD_INPUT = "//input[@name='password']"
    LOGIN_BUTTON = "//button[@type='submit' and normalize-space()='Sign in']"
    ERROR_MESSAGE = "[data-testid='error-message']"
    REMEMBER_ME_CHECKBOX = "[data-testid='remember-me']"
    FORGOT_PASSWORD_LINK = "[data-testid='forgot-password']"

    def __init__(self, page: Page, base_url: str) -> None:
        """Initialize login page.

        Args:
            page: Playwright page instance.
            base_url: Base URL for UI tests.
        """
        super().__init__(page, base_url)

    @allure.step("Enter email: {email}")
    def enter_email(self, email: str) -> "LoginPage":
        """Enter email in input field.

        Args:
            email: User email.

        Returns:
            Self for chaining.
        """
        self.fill(self.EMAIL_INPUT, email)
        return self

    @allure.step("Enter password")
    def enter_password(self, password: str) -> "LoginPage":
        """Enter password in input field.

        Args:
            password: User password.

        Returns:
            Self for chaining.
        """
        self.fill(self.PASSWORD_INPUT, password)
        return self

    @allure.step("Click login button")
    def click_login_button(self) -> None:
        """Click login button."""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Login with credentials: {email}")
    def login(self, email: str, password: str) -> None:
        """Perform login with credentials.

        Args:
            email: User email.
            password: User password.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    @allure.step("Check remember me checkbox")
    def check_remember_me(self) -> "LoginPage":
        """Check remember me checkbox.

        Returns:
            Self for chaining.
        """
        self.page.locator(self.REMEMBER_ME_CHECKBOX).check()
        return self

    @allure.step("Click forgot password link")
    def click_forgot_password(self) -> None:
        """Click forgot password link."""
        self.click(self.FORGOT_PASSWORD_LINK)

    def get_error_message(self) -> str:
        """Get error message text.

        Returns:
            Error message string.
        """
        return str(self.get_text(self.ERROR_MESSAGE))

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed.

        Returns:
            True if error message is visible.
        """
        return bool(self.is_visible(self.ERROR_MESSAGE))

    def assert_error_message(self, expected_text: str) -> None:
        """Assert error message contains expected text.

        Args:
            expected_text: Expected error message text.
        """
        self.assert_element_has_text(self.ERROR_MESSAGE, expected_text)

    def assert_login_page_loaded(self) -> None:
        """Assert login page is properly loaded."""
        self.assert_element_visible(self.EMAIL_INPUT)
        self.assert_element_visible(self.PASSWORD_INPUT)
        self.assert_element_visible(self.LOGIN_BUTTON)
