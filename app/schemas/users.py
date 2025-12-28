from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

from app.schemas.passports import PassportResponse


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)


class UserCreate(UserBase):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=100)


class PassportInUserCreate(BaseModel):
    passport_number: int = Field(..., gt=0)
    city: str = Field(..., min_length=1, max_length=30)


class UserCreateWithPassport(UserBase):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    passport: Optional[PassportInUserCreate] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=30)
    last_name: Optional[str] = Field(None, min_length=1, max_length=30)
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime


class MyProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime


class MyProfileUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)


class AdminProfileUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    role: Optional[str] = Field(None, pattern="^(user|admin)$")


class UserWithPassportResponse(UserResponse):
    passport: Optional["PassportResponse"] = None


class UsersListResponse(BaseModel):
    users: List[UserResponse]

