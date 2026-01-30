from jsonschema import validate

from config.settings import Settings
from src.api.contracts.auth import JWT_TOKEN_SCHEMA

HEALTH_RESPONSE_SCHEMA: dict[str, object] = {
    "type": "string",
    "minLength": 1,
}

COURSES_RESPONSE_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["courses"],
    "properties": {
        "courses": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "country", "language", "type", "startDate"],
                "properties": {
                    "name": {"type": "string"},
                    "country": {"type": "string"},
                    "language": {"type": "string"},
                    "type": {"type": "string"},
                    "startDate": {"type": "string"},
                },
            },
        }
    },
    "additionalProperties": True,
}

COURSE_TYPES_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["types"],
    "properties": {"types": {"type": "array", "items": {"type": "string"}}},
    "additionalProperties": True,
}

COURSE_LANGUAGES_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["languages"],
    "properties": {"languages": {"type": "array", "items": {"type": "string"}}},
    "additionalProperties": True,
}

COURSE_COUNTRIES_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["countries"],
    "properties": {"countries": {"type": "array", "items": {"type": "string"}}},
    "additionalProperties": True,
}


class ContractRegistry:
    """Registry for response contracts by method and path."""

    def __init__(self) -> None:
        self._schemas: dict[tuple[str, str], dict[str, object]] = {}

    def register(self, method: str, path: str, schema: dict[str, object]) -> None:
        self._schemas[(method.upper(), path)] = schema

    def validate(self, method: str, path: str, payload: object) -> None:
        schema = self._schemas.get((method.upper(), path))
        if not schema:
            return
        validate(instance=payload, schema=schema)


def build_default_registry(settings: Settings) -> ContractRegistry:
    registry = ContractRegistry()

    registry.register("POST", settings.auth_login_path, JWT_TOKEN_SCHEMA)
    registry.register("POST", settings.auth_register_path, JWT_TOKEN_SCHEMA)
    registry.register("GET", "/api/public/health", HEALTH_RESPONSE_SCHEMA)
    registry.register("GET", "/api/secured/health", HEALTH_RESPONSE_SCHEMA)

    registry.register("GET", "/api/secured/course", COURSES_RESPONSE_SCHEMA)
    registry.register("GET", "/api/secured/course/types", COURSE_TYPES_SCHEMA)
    registry.register("GET", "/api/secured/course/languages", COURSE_LANGUAGES_SCHEMA)
    registry.register("GET", "/api/secured/course/countries", COURSE_COUNTRIES_SCHEMA)
    registry.register("DELETE", "/api/secured/account/delete", {"type": "string"})

    return registry
