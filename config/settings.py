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
    default_timeout: int = Field(default=30000, description="Default timeout for UI actions")
    api_timeout: int = Field(default=10000, description="Default timeout for API requests")

    # Auth credentials (secrets)
    test_user_email: str = Field(default="", description="Test user email")
    test_user_password: SecretStr = Field(default="", description="Test user password")  # type: ignore[assignment]

    # JWT / OAuth settings
    jwt_secret: SecretStr = Field(default="", description="JWT secret key")  # type: ignore[assignment]
    oauth_client_id: str = Field(default="", description="OAuth client ID")
    oauth_client_secret: SecretStr = Field(default="", description="OAuth client secret")  # type: ignore[assignment]

    # Parallel execution
    workers: int = Field(default=4, description="Number of parallel workers")

    @property
    def api_timeout_seconds(self) -> float:
        """API timeout in seconds for httpx."""
        return self.api_timeout / 1000


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


settings = get_settings()
