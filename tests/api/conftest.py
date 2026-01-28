import contextlib
from collections.abc import Generator

import pytest

from src.api.client import APIClient
from src.api.endpoints.auth import AuthAPI
from src.api.endpoints.users import UsersAPI
from src.api.models.users import UserCreate, UserResponse


@pytest.fixture
def created_user(
    users_api: UsersAPI,
    user_data: UserCreate,
) -> Generator[UserResponse, None, None]:
    """Create user via API and return response.

    Args:
        users_api: Users API fixture.
        user_data: User data fixture.

    Yields:
        Created user response.
    """
    user = users_api.create_user(user_data)
    yield user
    # Cleanup: delete created user
    with contextlib.suppress(Exception):
        users_api.delete_user(user.id)


@pytest.fixture
def unauthenticated_users_api(api_client: APIClient) -> UsersAPI:
    """Create Users API without authentication.

    Args:
        api_client: API client fixture.

    Returns:
        Unauthenticated Users API.
    """
    return UsersAPI(api_client)


@pytest.fixture
def unauthenticated_auth_api(api_client: APIClient) -> AuthAPI:
    """Create Auth API without authentication.

    Args:
        api_client: API client fixture.

    Returns:
        Auth API instance.
    """
    return AuthAPI(api_client)
