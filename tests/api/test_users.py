import allure
import httpx
import pytest

from src.api.endpoints.users import UsersAPI
from src.api.models.users import UserCreate, UserResponse, UserUpdate


@allure.epic("API")
@allure.feature("Users")
@pytest.mark.api
class TestUsers:
    """Users API tests."""

    @allure.story("Create User")
    @allure.title("Create user with valid data")
    @pytest.mark.smoke
    def test_create_user_with_valid_data(
        self,
        users_api: UsersAPI,
        user_data: UserCreate,
    ) -> None:
        """Test successful user creation."""
        user = users_api.create_user(user_data)

        assert user.id is not None
        assert user.email == user_data.email
        assert user.first_name == user_data.first_name
        assert user.last_name == user_data.last_name
        assert user.is_active is True

        # Cleanup
        users_api.delete_user(user.id)

    @allure.story("Get User")
    @allure.title("Get user by ID")
    @pytest.mark.smoke
    def test_get_user_by_id(
        self,
        users_api: UsersAPI,
        created_user: UserResponse,
    ) -> None:
        """Test getting user by ID."""
        user = users_api.get_user(created_user.id)

        assert user.id == created_user.id
        assert user.email == created_user.email

    @allure.story("Get User")
    @allure.title("Get non-existent user returns 404")
    def test_get_non_existent_user(self, users_api: UsersAPI) -> None:
        """Test getting non-existent user returns 404."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            users_api.get_user(user_id=999999)

        assert exc_info.value.response.status_code == 404

    @allure.story("Update User")
    @allure.title("Update user first name")
    def test_update_user_first_name(
        self,
        users_api: UsersAPI,
        created_user: UserResponse,
    ) -> None:
        """Test updating user first name."""
        update_data = UserUpdate(first_name="UpdatedName")

        updated_user = users_api.update_user(created_user.id, update_data)

        assert updated_user.first_name == "UpdatedName"
        assert updated_user.last_name == created_user.last_name

    @allure.story("Delete User")
    @allure.title("Delete user successfully")
    def test_delete_user(
        self,
        users_api: UsersAPI,
        user_data: UserCreate,
    ) -> None:
        """Test successful user deletion."""
        user = users_api.create_user(user_data)

        users_api.delete_user(user.id)

        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            users_api.get_user(user.id)
        assert exc_info.value.response.status_code == 404

    @allure.story("List Users")
    @allure.title("Get users list with pagination")
    def test_get_users_list_pagination(self, users_api: UsersAPI) -> None:
        """Test getting paginated users list."""
        response = users_api.get_users(page=1, per_page=10)

        assert response.page == 1
        assert response.per_page == 10
        assert response.total >= 0
        assert isinstance(response.items, list)
