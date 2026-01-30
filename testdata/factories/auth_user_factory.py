from dataclasses import dataclass

from faker import Faker

from config.settings import Settings

fake = Faker()


@dataclass(frozen=True)
class AuthUserData:
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: str


class AuthUserFactory:
    """Factory for auth user test data."""

    @staticmethod
    def build(settings: Settings) -> AuthUserData:
        email = settings.test_user_email or fake.email(domain="example.com")
        password = settings.test_user_password.get_secret_value() or "Password123"
        first_name = settings.test_user_first_name or fake.first_name()
        last_name = settings.test_user_last_name or fake.last_name()
        date_of_birth = settings.test_user_date_of_birth or "01.08.2001"
        return AuthUserData(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
