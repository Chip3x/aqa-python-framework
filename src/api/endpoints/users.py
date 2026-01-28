import allure

from src.api.client import APIClient
from src.api.models.users import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)


class UsersAPI:
    """Users API endpoints."""

    def __init__(self, client: APIClient) -> None:
        """Initialize Users API.

        Args:
            client: API client instance.
        """
        self.client = client
        self._base_path = "/users"

    @allure.step("Get user by ID: {user_id}")
    def get_user(self, user_id: int) -> UserResponse:
        """Get user by ID.

        Args:
            user_id: User ID.

        Returns:
            User response.
        """
        response = self.client.get(f"{self._base_path}/{user_id}")
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    @allure.step("Get users list")
    def get_users(self, page: int = 1, per_page: int = 10) -> UserListResponse:
        """Get paginated users list.

        Args:
            page: Page number.
            per_page: Items per page.

        Returns:
            User list response.
        """
        response = self.client.get(
            self._base_path,
            params={"page": page, "per_page": per_page},
        )
        response.raise_for_status()
        return UserListResponse.model_validate(response.json())

    @allure.step("Create user with email: {user_data.email}")
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create new user.

        Args:
            user_data: User creation data.

        Returns:
            Created user response.
        """
        response = self.client.post(self._base_path, json=user_data.model_dump())
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    @allure.step("Update user: {user_id}")
    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update existing user.

        Args:
            user_id: User ID.
            user_data: User update data.

        Returns:
            Updated user response.
        """
        response = self.client.patch(
            f"{self._base_path}/{user_id}",
            json=user_data.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    @allure.step("Delete user: {user_id}")
    def delete_user(self, user_id: int) -> None:
        """Delete user by ID.

        Args:
            user_id: User ID.
        """
        response = self.client.delete(f"{self._base_path}/{user_id}")
        response.raise_for_status()
