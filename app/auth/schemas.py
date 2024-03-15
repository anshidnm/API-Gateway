from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserCreateSchema(BaseModel):
    username: str
    name: str
    email: EmailStr
    mobile: str = Field(min_length=10, max_length=10)
    password: str = Field(min_length=8)
    profile_pic: str|None = None


class UserSchema(BaseModel):
    id: int
    username: str
    name: str
    email: str
    mobile: str
    profile_pic: str|None
    is_superuser: bool
    is_staff: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class config:
        from_attributes = True


class UserPasswordLoginSchema(BaseModel):
    username: str
    password: str


class RefreshTokenSchema(BaseModel):
    refresh: str