import allure
import pytest

from src.api.sdk import ApiContext


@allure.epic("API")
@allure.feature("Demo")
@pytest.mark.api
class TestDemoAPI:
    """Demo API tests."""

    @allure.story("Public")
    @allure.title("Public health check")
    @pytest.mark.smoke
    def test_public_health(self, api_context: ApiContext) -> None:
        """Verify public health endpoint is available."""
        body = api_context.services.health.public_health()
        assert body != ""

    @allure.story("Secured")
    @allure.title("Secured health check with JWT")
    @pytest.mark.smoke
    def test_secured_health_with_token(
        self,
        api_context: ApiContext,
        registered_user,
    ) -> None:
        """Register, login, and access secured endpoint."""
        body = api_context.services.health.secured_health(registered_user.token)
        assert body != ""
