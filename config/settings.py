from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=(CONFIG_DIR / ".env", CONFIG_DIR / "environments" / "dev.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Environment
    env: Literal["dev", "staging"] = Field(default="dev", description="Current environment")

    # Application URLs
    base_url: str = Field(default="https://example.com", description="Base URL for UI tests")
    api_url: str = Field(default="https://api.example.com", description="Base URL for API tests")

    # Browser settings
    browser: Literal["chromium", "firefox", "webkit"] = Field(
        default="chromium", description="Browser for UI tests"
    )
    headless: bool = Field(default=True, description="Run browser in headless mode")
    slow_mo: int = Field(default=0, description="Slow down browser actions by ms")

    # Timeouts (in milliseconds)
    default_timeout: int = Field(default=15000, description="Default timeout for UI actions")
    api_timeout: int = Field(default=10000, description="Default timeout for API requests")

    # Auth credentials (secrets)
    test_user_email: str = Field(default="", description="Test user email")
    test_user_password: SecretStr = Field(default=SecretStr(""), description="Test user password")
    test_user_first_name: str = Field(default="", description="Test user first name")
    test_user_last_name: str = Field(default="", description="Test user last name")
    test_user_date_of_birth: str = Field(
        default="", description="Test user date of birth (DD.MM.YYYY)"
    )

    # Auth endpoints / token mapping
    auth_login_path: str = Field(default="/api/public/login", description="Auth login path")
    auth_register_path: str = Field(
        default="/api/public/registration", description="Auth register path"
    )
    auth_token_field: str = Field(default="jwt-token", description="JWT token field name")

    # Logging
    log_sensitive: bool = Field(default=False, description="Allow logging sensitive data")

    # Parallel execution
    workers: int = Field(default=4, description="Number of parallel workers")

    @property
    def api_timeout_seconds(self) -> float:
        """API timeout in seconds for httpx."""
        return self.api_timeout / 1000

    def validate_runtime(self) -> None:
        """Validate required runtime configuration."""
        if not self.api_url:
            raise ValueError("API_URL is required")
        if not self.base_url:
            raise ValueError("BASE_URL is required")
        if not self.auth_login_path.startswith("/"):
            raise ValueError("AUTH_LOGIN_PATH must start with '/'")
        if not self.auth_register_path.startswith("/"):
            raise ValueError("AUTH_REGISTER_PATH must start with '/'")
        if not self.auth_token_field:
            raise ValueError("AUTH_TOKEN_FIELD is required")


@lru_cache
def get_settings(env: str | None = None) -> Settings:
    """Get cached settings instance.
    Args:
        env: Optional environment name to load specific env file.
    Returns:
        Settings instance with loaded configuration.
    """
    if env:
        env_file = CONFIG_DIR / "environments" / f"{env}.env"
        return Settings(
            _env_file=(CONFIG_DIR / ".env", env_file),
        )
    return Settings()
