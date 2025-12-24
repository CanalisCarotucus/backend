from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.database.models import Passport


class PassportRepository(BaseRepository[Passport]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = Passport

    async def get_by_id(self, passport_id: int) -> Optional[Passport]:
        query = select(self.model).where(self.model.id == passport_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[Passport]:
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Passport]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, passport_data: dict) -> Passport:
        passport = self.model(**passport_data)
        self.db.add(passport)
        await self.db.flush()
        await self.db.refresh(passport)
        return passport

    async def update(self, passport_id: int, passport_data: dict) -> Optional[Passport]:
        passport = await self.get_by_id(passport_id)
        if passport is None:
            return None

        for key, value in passport_data.items():
            setattr(passport, key, value)

        await self.db.flush()
        await self.db.refresh(passport)
        return passport

    async def delete(self, passport_id: int) -> bool:
        passport = await self.get_by_id(passport_id)
        if passport is None:
            return False

        await self.db.delete(passport)
        await self.db.flush()
        return True

