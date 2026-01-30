from collections.abc import Generator
from typing import Any

import pytest

from config.settings import Settings, get_settings
from src.utils.test_data_manager import TestDataManager

# Import all fixtures from fixtures module
pytest_plugins = [
    "fixtures.api_fixtures",
    "fixtures.ui_fixtures",
    "fixtures.data_fixtures",
]


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=["dev", "staging"],
        help="Environment to run tests against (default: dev)",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser for UI tests (default: chromium)",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.fixture(scope="session")
def settings(request: pytest.FixtureRequest) -> Settings:
    """Get settings for current environment.

    Args:
        request: Pytest request with CLI options.

    Returns:
        Settings instance.
    """
    env = request.config.getoption("--env")
    # Clear cache to reload settings
    get_settings.cache_clear()
    loaded_settings = get_settings(env)
    loaded_settings.validate_runtime()
    return loaded_settings


@pytest.fixture(scope="session", autouse=True)
def configure_settings(request: pytest.FixtureRequest, settings: Settings) -> None:
    """Configure settings from CLI options.

    Args:
        request: Pytest request with CLI options.
    """
    # Override browser if specified
    browser = request.config.getoption("--browser")
    if browser:
        object.__setattr__(settings, "browser", browser)

    # Override headless if --headed specified
    if request.config.getoption("--headed"):
        object.__setattr__(settings, "headless", False)


@pytest.fixture
def test_data_manager() -> Generator[TestDataManager, None, None]:
    """Create test data manager and cleanup after test."""
    manager = TestDataManager()
    yield manager
    manager.cleanup_all()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item) -> Generator[None, Any, None]:
    """Store test result for fixture access (screenshot on failure).

    Args:
        item: Test item.
    """
    outcome: Any = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
