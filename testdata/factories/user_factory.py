from faker import Faker

from src.api.models.users import UserCreate, UserResponse, UserUpdate

fake = Faker()


class UserFactory:
    """Factory for generating user test data."""

    @staticmethod
    def build_email(domain: str = "test.com") -> str:
        """Generate random email.

        Args:
            domain: Email domain.

        Returns:
            Random email address.
        """
        return str(fake.email(domain=domain))

    @staticmethod
    def build_password(length: int = 12) -> str:
        """Generate random password.

        Args:
            length: Password length.

        Returns:
            Random password.
        """
        return str(fake.password(length=length, special_chars=True, digits=True, upper_case=True))

    @staticmethod
    def build_create(
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        password: str | None = None,
    ) -> UserCreate:
        """Build user creation data.

        Args:
            email: Optional email override.
            first_name: Optional first name override.
            last_name: Optional last name override.
            password: Optional password override.

        Returns:
            User creation model.
        """
        return UserCreate(
            email=email or fake.email(),
            first_name=first_name or fake.first_name(),
            last_name=last_name or fake.last_name(),
            password=password or fake.password(length=12),
        )

    @staticmethod
    def build_update(
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> UserUpdate:
        """Build user update data.

        Args:
            first_name: Optional first name.
            last_name: Optional last name.
            email: Optional email.

        Returns:
            User update model.
        """
        return UserUpdate(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

    @staticmethod
    def build_response(
        user_id: int | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        is_active: bool = True,
    ) -> UserResponse:
        """Build user response data for mocking.

        Args:
            user_id: Optional user ID.
            email: Optional email.
            first_name: Optional first name.
            last_name: Optional last name.
            is_active: Active status.

        Returns:
            User response model.
        """
        return UserResponse(
            id=user_id or fake.random_int(min=1, max=10000),
            email=email or fake.email(),
            first_name=first_name or fake.first_name(),
            last_name=last_name or fake.last_name(),
            is_active=is_active,
        )

    @staticmethod
    def build_admin(
        email: str | None = None,
        password: str | None = None,
    ) -> UserCreate:
        """Build admin user data.

        Args:
            email: Optional email override.
            password: Optional password override.

        Returns:
            Admin user creation model.
        """
        return UserCreate(
            email=email or f"admin_{fake.user_name()}@test.com",
            first_name="Admin",
            last_name=fake.last_name(),
            password=password or fake.password(length=16),
        )
