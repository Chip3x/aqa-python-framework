from collections.abc import Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.settings import Settings
from src.ui.pages.dashboard_page import DashboardPage
from src.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Create Playwright instance for session.

    Yields:
        Playwright instance.
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(settings: Settings, playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Launch browser based on settings.

    Args:
        playwright_instance: Playwright fixture.

    Yields:
        Browser instance.
    """
    browser_type = getattr(playwright_instance, settings.browser)
    browser = browser_type.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo,
    )
    yield browser
    browser.close()


@pytest.fixture
def context(settings: Settings, browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create browser context for test isolation.

    Args:
        browser: Browser fixture.

    Yields:
        Browser context.
    """
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
    )
    context.set_default_timeout(settings.default_timeout)
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    """Create page with screenshot on failure.

    Args:
        context: Browser context fixture.
        request: Pytest request for test info.

    Yields:
        Page instance.
    """
    page = context.new_page()
    yield page

    # Screenshot on failure
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"screenshot_{request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )

    page.close()


@pytest.fixture
def login_page(settings: Settings, page: Page) -> LoginPage:
    """Create login page object.

    Args:
        page: Page fixture.

    Returns:
        Login page instance.
    """
    return LoginPage(page, settings.base_url)


@pytest.fixture
def dashboard_page(settings: Settings, page: Page) -> DashboardPage:
    """Create dashboard page object.

    Args:
        page: Page fixture.

    Returns:
        Dashboard page instance.
    """
    return DashboardPage(page, settings.base_url)


@pytest.fixture
def authenticated_page(settings: Settings, page: Page, login_page: LoginPage) -> Page:
    """Create page with authenticated user.

    Args:
        page: Page fixture.
        login_page: Login page fixture.

    Returns:
        Authenticated page.
    """
    login_page.open()
    login_page.login(
        settings.test_user_email,
        settings.test_user_password.get_secret_value(),
    )
    page.wait_for_url(f"*{DashboardPage.url_path}*")
    return page
