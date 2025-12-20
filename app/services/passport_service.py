from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.database.models import Passport, User
from app.exceptions import UserNotFound, PassportAlreadyExists


class PassportService:
    async def get_passport(self, db: AsyncSession, passport_id: int) -> Optional[Passport]:
        query = select(Passport).where(Passport.id == passport_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_passport_by_user_id(self, db: AsyncSession, user_id: int) -> Optional[Passport]:
        query = select(Passport).where(Passport.user_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create_passport_for_user(
        self, db: AsyncSession, user_id: int, passport_data: dict
    ) -> Passport:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")

        existing = await self.get_passport_by_user_id(db, user_id)
        if existing:
            raise PassportAlreadyExists(f"User with id {user_id} already has a passport")

        passport_data["user_id"] = user_id
        passport = Passport(**passport_data)
        db.add(passport)
        await db.flush()
        await db.refresh(passport)
        return passport

    async def update_passport(
        self, db: AsyncSession, passport_id: int, passport_data: dict
    ) -> Optional[Passport]:
        passport = await self.get_passport(db, passport_id)
        if passport is None:
            return None

        for key, value in passport_data.items():
            setattr(passport, key, value)

        await db.flush()
        await db.refresh(passport)
        return passport

    async def delete_passport(self, db: AsyncSession, passport_id: int) -> bool:
        passport = await self.get_passport(db, passport_id)
        if passport is None:
            return False

        await db.delete(passport)
        await db.flush()
        return True


passport_service = PassportService()
