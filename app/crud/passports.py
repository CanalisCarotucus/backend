from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Passport, User
from app.core.exceptions import UserNotFound, PassportNotFound, PassportAlreadyExists
from app.schemas.passports import (
    PassportCreate, PassportCreateWithUser, PassportUpdate, PassportResponse
)


class PassportCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_by_id_orm(self, passport_id: int) -> Passport:
        query = select(Passport).where(Passport.id == passport_id)
        result = await self.db.execute(query)
        passport = result.scalar_one_or_none()
        if passport is None:
            raise PassportNotFound(f"Passport with id {passport_id} not found")
        return passport

    async def get_by_id(self, passport_id: int) -> PassportResponse:
        passport = await self._get_by_id_orm(passport_id)
        return PassportResponse.model_validate(passport)

    async def get_by_user_id(self, user_id: int) -> Optional[PassportResponse]:
        query = select(Passport).where(Passport.user_id == user_id)
        result = await self.db.execute(query)
        passport = result.scalar_one_or_none()
        if passport is None:
            return None
        return PassportResponse.model_validate(passport)

    async def _get_by_user_id_orm(self, user_id: int) -> Optional[Passport]:
        query = select(Passport).where(Passport.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[PassportResponse]:
        result = await self.db.execute(select(Passport))
        passports = list(result.scalars().all())
        return [PassportResponse.model_validate(p) for p in passports]

    async def _create_orm(self, passport_data: dict) -> Passport:
        passport = Passport(**passport_data)
        self.db.add(passport)
        await self.db.flush()
        await self.db.refresh(passport)
        return passport

    async def create(self, passport_data: PassportCreate) -> PassportResponse:
        passport_dict = passport_data.model_dump()
        passport = await self._create_orm(passport_dict)
        return PassportResponse.model_validate(passport)

    async def update(self, passport_id: int, passport_data: PassportUpdate) -> PassportResponse:
        passport = await self._get_by_id_orm(passport_id)
        
        update_dict = passport_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(passport, key, value)

        await self.db.flush()
        await self.db.refresh(passport)
        return PassportResponse.model_validate(passport)

    async def delete(self, passport_id: int) -> None:
        passport = await self._get_by_id_orm(passport_id)
        await self.db.delete(passport)
        await self.db.flush()

    async def create_for_user(self, user_id: int, passport_data: dict) -> Passport:
        user_query = select(User).where(User.id == user_id)
        user_result = await self.db.execute(user_query)
        user = user_result.scalar_one_or_none()
        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")

        existing = await self._get_by_user_id_orm(user_id)
        if existing:
            raise PassportAlreadyExists(f"User with id {user_id} already has a passport")

        passport_data["user_id"] = user_id
        return await self._create_orm(passport_data)

    async def create_for_user_from_schema(
        self, passport_data: PassportCreateWithUser
    ) -> PassportResponse:
        passport_dict = passport_data.model_dump(exclude={"user_id"})
        passport_orm = await self.create_for_user(passport_data.user_id, passport_dict)
        return PassportResponse.model_validate(passport_orm)
