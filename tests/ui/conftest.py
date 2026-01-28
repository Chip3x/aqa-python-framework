import pytest
from playwright.sync_api import Page

from src.ui.components.header import Header
from src.ui.components.sidebar import Sidebar
from src.ui.pages.dashboard_page import DashboardPage


@pytest.fixture
def header(page: Page) -> Header:
    """Create header component.

    Args:
        page: Page fixture.

    Returns:
        Header component instance.
    """
    return Header(page)


@pytest.fixture
def sidebar(page: Page) -> Sidebar:
    """Create sidebar component.

    Args:
        page: Page fixture.

    Returns:
        Sidebar component instance.
    """
    return Sidebar(page)


@pytest.fixture
def logged_in_dashboard(authenticated_page: Page) -> DashboardPage:
    """Get dashboard page after login.

    Args:
        authenticated_page: Authenticated page fixture.

    Returns:
        Dashboard page instance.
    """
    return DashboardPage(authenticated_page)
