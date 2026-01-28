from collections.abc import Generator

import pytest

from src.api.client import APIClient
from src.api.endpoints.auth import AuthAPI
from src.api.endpoints.users import UsersAPI
from src.utils.auth_helper import AuthHelper


@pytest.fixture
def api_client() -> Generator[APIClient, None, None]:
    """Create API client instance.

    Yields:
        API client.
    """
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def auth_helper(api_client: APIClient) -> AuthHelper:
    """Create auth helper with API client.

    Args:
        api_client: API client fixture.

    Returns:
        Auth helper instance.
    """
    return AuthHelper(api_client)


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
def oauth_client(auth_helper: AuthHelper) -> APIClient:
    """Create API client authenticated with OAuth.

    Args:
        auth_helper: Auth helper fixture.

    Returns:
        OAuth authenticated API client.
    """
    auth_helper.login_with_oauth()
    return auth_helper.client


@pytest.fixture
def auth_api(api_client: APIClient) -> AuthAPI:
    """Create Auth API instance.

    Args:
        api_client: API client fixture.

    Returns:
        Auth API instance.
    """
    return AuthAPI(api_client)


@pytest.fixture
def users_api(authenticated_client: APIClient) -> UsersAPI:
    """Create Users API instance with authenticated client.

    Args:
        authenticated_client: Authenticated API client fixture.

    Returns:
        Users API instance.
    """
    return UsersAPI(authenticated_client)
