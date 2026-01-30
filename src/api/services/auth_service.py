from config.settings import Settings
from src.api.contracts.registry import ContractRegistry
from src.api.endpoints.auth import AuthAPI


class AuthService:
    """Auth service with contract validation."""

    def __init__(
        self,
        auth_api: AuthAPI,
        settings: Settings,
        contracts: ContractRegistry,
    ) -> None:
        self._auth_api = auth_api
        self._settings = settings
        self._contracts = contracts

    def login(self, email: str, password: str) -> str:
        payload = self._auth_api.login_response(email, password)
        self._contracts.validate("POST", self._settings.auth_login_path, payload)
        return self._auth_api.extract_token(payload)

    def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
    ) -> str:
        payload = self._auth_api.register_response(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        self._contracts.validate("POST", self._settings.auth_register_path, payload)
        return self._auth_api.extract_token(payload)
