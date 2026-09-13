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


class MorningCheckin(BaseModel):
    sleep_duration: float
    sleep_quality: int
    energy: int
    recorded_at: datetime | None = None

    @field_validator("sleep_duration")
    @classmethod
    def sleep_range(cls, value: float) -> float:
        if not 0 <= value <= 24:
            raise ValueError("sleep_duration must be between 0 and 24")
        return value

    @field_validator("sleep_quality", "energy")
    @classmethod
    def score_range(cls, value: int) -> int:
        if not 1 <= value <= 10:
            raise ValueError("score must be between 1 and 10")
        return value


class EveningCheckin(BaseModel):
    mood: int
    stress: int
    focus: int
    activity_duration: float | None = None
    recorded_at: datetime | None = None

    @field_validator("mood", "stress", "focus")
    @classmethod
    def score_range(cls, value: int) -> int:
        if not 1 <= value <= 10:
            raise ValueError("score must be between 1 and 10")
        return value

    @field_validator("activity_duration")
    @classmethod
    def activity_range(cls, value: float | None) -> float | None:
        if value is not None and not 0 <= value <= 1440:
            raise ValueError("activity_duration must be between 0 and 1440")
        return value


class TimelineItem(BaseModel):
    recorded_at: datetime
    observation_type: str
    value: float | str | bool


class Insight(BaseModel):
    code: str
    title: str
    message: str
    evidence_count: int
