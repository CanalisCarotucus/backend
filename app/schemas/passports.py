from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PassportBase(BaseModel):
    passport_number: int = Field(..., gt=0)
    city: str = Field(..., min_length=1, max_length=30)


class PassportCreate(PassportBase):
    pass


class PassportCreateWithUser(BaseModel):
    passport_number: int = Field(..., gt=0)
    city: str = Field(..., min_length=1, max_length=30)
    user_id: int = Field(..., gt=0)


class PassportUpdate(BaseModel):
    passport_number: Optional[int] = Field(None, gt=0)
    city: Optional[str] = Field(None, min_length=1, max_length=30)


class PassportResponse(PassportBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

