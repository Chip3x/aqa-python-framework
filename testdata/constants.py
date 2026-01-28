"""Test data constants and enums."""

from enum import Enum


class UserRole(str, Enum):
    """User role enum."""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class HttpStatus:
    """HTTP status codes."""

    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500


class ErrorMessages:
    """Common error messages for assertions."""

    INVALID_CREDENTIALS = "Invalid email or password"
    USER_NOT_FOUND = "User not found"
    EMAIL_ALREADY_EXISTS = "Email already exists"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Access denied"
    VALIDATION_ERROR = "Validation error"


class TestUserCredentials:
    """Test user credentials (non-sensitive defaults)."""

    DEFAULT_PASSWORD = "TestPassword123!"
    INVALID_PASSWORD = "wrong_password"
    WEAK_PASSWORD = "123"


class Timeouts:
    """Timeout constants in milliseconds."""

    SHORT = 5000
    MEDIUM = 15000
    LONG = 30000
    EXTRA_LONG = 60000


class Pagination:
    """Pagination defaults."""

    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    MAX_PER_PAGE = 100
