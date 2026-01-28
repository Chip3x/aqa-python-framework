import pytest

from src.api.models.users import UserCreate
from testdata.factories.user_factory import UserFactory


@pytest.fixture
def user_data() -> UserCreate:
    """Generate random user data.

    Returns:
        User creation data.
    """
    return UserFactory.build_create()


@pytest.fixture
def user_data_batch() -> list[UserCreate]:
    """Generate batch of random user data.

    Returns:
        List of user creation data.
    """
    return [UserFactory.build_create() for _ in range(5)]


@pytest.fixture
def admin_user_data() -> UserCreate:
    """Generate admin user data.

    Returns:
        Admin user creation data.
    """
    return UserFactory.build_admin()


@pytest.fixture
def test_email() -> str:
    """Generate random test email.

    Returns:
        Random email address.
    """
    return UserFactory.build_email()


@pytest.fixture
def test_password() -> str:
    """Generate random test password.

    Returns:
        Random password.
    """
    return UserFactory.build_password()
