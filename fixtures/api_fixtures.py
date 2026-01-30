from collections.abc import Generator

import pytest

from config.settings import Settings
from src.api.client import APIClient
from src.api.endpoints.auth import AuthAPI
from src.api.endpoints.users import UsersAPI
from src.api.sdk import ApiContext
from src.utils.auth_helper import AuthHelper


@pytest.fixture
def api_client(settings: Settings) -> Generator[APIClient, None, None]:
    """Create API client instance.

    Yields:
        API client.
    """
    client = APIClient(settings=settings)
    yield client
    client.close()


@pytest.fixture
def api_context(settings: Settings) -> Generator[ApiContext, None, None]:
    """Create API context with client and endpoints."""
    context = ApiContext(settings)
    yield context
    context.close()


@pytest.fixture
def auth_helper(settings: Settings, api_client: APIClient) -> AuthHelper:
    """Create auth helper with API client.

    Args:
        api_client: API client fixture.

    Returns:
        Auth helper instance.
    """
    return AuthHelper(settings, api_client)


@pytest.fixture
def authenticated_client(auth_helper: AuthHelper) -> APIClient:
    """Create authenticated API client using test user.

    Args:
        auth_helper: Auth helper fixture.

    Returns:
        Authenticated API client.
    """
    auth_helper.login_as_test_user()
    return auth_helper.client


@pytest.fixture
def auth_api(settings: Settings, api_client: APIClient) -> AuthAPI:
    """Create Auth API instance.

    Args:
        api_client: API client fixture.

    Returns:
        Auth API instance.
    """
    return AuthAPI(api_client, settings)


@pytest.fixture
def users_api(authenticated_client: APIClient) -> UsersAPI:
    """Create Users API instance with authenticated client.

    Args:
        authenticated_client: Authenticated API client fixture.

    Returns:
        Users API instance.
    """
    return UsersAPI(authenticated_client)
