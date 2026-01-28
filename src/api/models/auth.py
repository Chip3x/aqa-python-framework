from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request model."""

    email: EmailStr
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    """Login response model."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None
    refresh_token: str | None = None


class TokenRefreshRequest(BaseModel):
    """Token refresh request model."""

    refresh_token: str


class OAuthTokenRequest(BaseModel):
    """OAuth token request model."""

    grant_type: str = "client_credentials"
    client_id: str
    client_secret: str
    scope: str | None = None


class OAuthTokenResponse(BaseModel):
    """OAuth token response model."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    scope: str | None = None
