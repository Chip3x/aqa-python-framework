from typing import Any, cast

import allure

from config.settings import Settings
from src.api.client import APIClient
from src.api.models.auth import LoginCredentials, UserProfileCreateRequest


class AuthAPI:
    """Authentication API endpoints."""

    def __init__(self, client: APIClient, settings: Settings) -> None:
        """Initialize Auth API.

        Args:
            client: API client instance.
            settings: Settings instance.
        """
        self.client = client
        self._settings = settings

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str) -> str:
        """Authenticate user with email and password.

        Args:
            email: User email.
            password: User password.

        Returns:
            JWT token string.
        """
        payload = self.login_response(email, password)
        return self._extract_token(payload)

    @allure.step("Register user with email: {email}")
    def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
    ) -> str:
        """Register user.

        Args:
            email: User email.
            password: User password.
            first_name: User first name.
            last_name: User last name.
            date_of_birth: Date of birth in DD.MM.YYYY format.

        Returns:
            JWT token string.
        """
        payload = self.register_response(email, password, first_name, last_name, date_of_birth)
        return self._extract_token(payload)

    @allure.step("Login response with email: {email}")
    def login_response(self, email: str, password: str) -> dict[str, Any]:
        """Return raw login response payload."""
        request = LoginCredentials(email=email, password=password)
        response = self.client.post(self._settings.auth_login_path, json=request.model_dump())
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    @allure.step("Register response with email: {email}")
    def register_response(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
    ) -> dict[str, Any]:
        """Return raw registration response payload."""
        request = UserProfileCreateRequest(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        response = self.client.post(
            self._settings.auth_register_path,
            json=request.model_dump(by_alias=True),
        )
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def _extract_token(self, payload: dict[str, object]) -> str:
        token_field = self._settings.auth_token_field
        raw_token = payload.get(token_field)
        if not isinstance(raw_token, str) or not raw_token:
            raise ValueError(f"Token field '{token_field}' not found in response")
        return raw_token

    def extract_token(self, payload: dict[str, object]) -> str:
        """Public token extractor for service layer."""
        return self._extract_token(payload)
