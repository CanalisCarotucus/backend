from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.database.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = User

    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(self.model).where(self.model.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_with_passport(self, user_id: int) -> Optional[User]:
        query = select(self.model).where(self.model.id == user_id).options(
            selectinload(self.model.passport)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[User]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, user_data: dict) -> User:
        user = self.model(**user_data)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_data: dict) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user is None:
            return False

        await self.db.delete(user)
        await self.db.flush()
        return True

