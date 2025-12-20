from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.passports import PassportResponse


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)


class UserCreate(UserBase):
    pass


class PassportInUserCreate(BaseModel):
    passport_number: int = Field(..., gt=0)
    city: str = Field(..., min_length=1, max_length=30)


class UserCreateWithPassport(UserBase):
    passport: Optional[PassportInUserCreate] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=30)
    last_name: Optional[str] = Field(None, min_length=1, max_length=30)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserWithPassportResponse(UserResponse):
    passport: Optional["PassportResponse"] = None


class UsersListResponse(BaseModel):
    users: List[UserResponse]
