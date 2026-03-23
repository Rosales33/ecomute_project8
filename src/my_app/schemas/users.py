from pydantic import BaseModel, field_validator, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user"""

    username: str
    email: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not v.isalnum():
            raise ValueError("Password must be alphanumeric")
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True) #This configuration allows the Pydantic model to be created from an ORM object, which is useful when we want to return database models directly as API responses.
