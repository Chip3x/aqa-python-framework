from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginCredentials(BaseModel):
    """Login request model."""

    email: EmailStr
    password: str = Field(min_length=1)


class UserProfileCreateRequest(BaseModel):
    """User registration request model."""

    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(alias="firstName", min_length=1, max_length=255)
    last_name: str = Field(alias="lastName", min_length=1, max_length=255)
    email: EmailStr
    date_of_birth: str = Field(alias="dateOfBirth", min_length=1, max_length=20)
    password: str = Field(min_length=1, max_length=20)


class JwtTokenResponse(BaseModel):
    """JWT token response model."""

    model_config = ConfigDict(populate_by_name=True)

    jwt_token: str = Field(alias="jwt-token")
