import contextlib
from collections.abc import Generator
from dataclasses import dataclass

import pytest

from config.settings import Settings
from src.api.client import APIClient
from src.api.contracts.registry import build_default_registry
from src.api.endpoints.auth import AuthAPI
from src.api.endpoints.users import UsersAPI
from src.api.models.users import UserCreate, UserResponse
from src.api.sdk import ApiContext
from src.utils.test_data_manager import TestDataManager
from testdata.factories.auth_user_factory import AuthUserData, AuthUserFactory


@dataclass(frozen=True)
class RegisteredUser:
    user: AuthUserData
    token: str


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
def unauthenticated_auth_api(settings: Settings, api_client: APIClient) -> AuthAPI:
    """Create Auth API without authentication.

    Args:
        api_client: API client fixture.

    Returns:
        Auth API instance.
    """
    return AuthAPI(api_client, settings)


@pytest.fixture
def registered_user(
    settings: Settings,
    api_context: ApiContext,
    test_data_manager: TestDataManager,
) -> RegisteredUser:
    """Register a user and cleanup after test."""
    user = AuthUserFactory.build(settings)
    token = api_context.services.auth.register(
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
    )
    registered = RegisteredUser(user=user, token=token)

    def _cleanup() -> None:
        cleanup_client = APIClient(settings=settings)
        try:
            cleanup_client.set_token(token)
            contracts = build_default_registry(settings)
            from src.api.services.account_service import AccountService

            AccountService(cleanup_client, contracts).delete_current()
        finally:
            cleanup_client.close()

    test_data_manager.register_cleanup(_cleanup)
    return registered
