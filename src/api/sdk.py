from config.settings import Settings
from src.api.client import APIClient
from src.api.contracts.registry import ContractRegistry, build_default_registry
from src.api.endpoints.account import AccountAPI
from src.api.endpoints.auth import AuthAPI
from src.api.services import AccountService, AuthService, CoursesService, HealthService


class ApiContext:
    """API SDK context holding client and endpoints."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = APIClient(settings=settings)
        self.contracts: ContractRegistry = build_default_registry(settings)
        self.auth = AuthAPI(self.client, settings)
        self.account = AccountAPI(self.client)
        self.services = ApiServices(self)

    def close(self) -> None:
        """Close underlying HTTP client."""
        self.client.close()


class ApiServices:
    """High-level services for tests."""

    def __init__(self, context: ApiContext) -> None:
        self.auth = AuthService(context.auth, context.settings, context.contracts)
        self.health = HealthService(context.client, context.contracts)
        self.courses = CoursesService(context.client, context.contracts)
        self.account = AccountService(context.client, context.contracts)
