from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

class ProfileUpdate(BaseModel):
    display_name: str | None = None
    date_of_birth: str | None = None
    sex_at_birth: str | None = None

class ProfileResponse(ProfileUpdate):
    model_config = ConfigDict(from_attributes=True)
    user_id: int

class ObservationCreate(BaseModel):
    observation_type: str
    numeric_value: float | None = None
    text_value: str | None = None
    boolean_value: bool | None = None
    recorded_at: datetime

class ObservationResponse(BaseModel):
    id: int
    observation_type: str
    numeric_value: float | None
    text_value: str | None
    boolean_value: bool | None
    recorded_at: datetime
