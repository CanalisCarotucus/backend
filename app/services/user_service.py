from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.database.models import User, Passport


class UserService:
    async def get_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_with_passport(self, db: AsyncSession, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id).options(selectinload(User.passport))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_users(self, db: AsyncSession) -> List[User]:
        result = await db.execute(select(User))
        return list(result.scalars().all())

    async def create_user(self, db: AsyncSession, user_data: dict) -> User:
        user = User(**user_data)
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def create_user_with_passport(
        self, db: AsyncSession, user_data: dict, passport_data: dict
    ) -> User:
        user = User(**user_data)
        db.add(user)
        await db.flush()

        passport_data["user_id"] = user.id
        passport = Passport(**passport_data)
        db.add(passport)
        await db.flush()

        await db.refresh(user, ["passport"])
        return user

    async def update_user(
        self, db: AsyncSession, user_id: int, user_data: dict
    ) -> Optional[User]:
        user = await self.get_user(db, user_id)
        if user is None:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        await db.flush()
        await db.refresh(user)
        return user

    async def delete_user(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get_user(db, user_id)
        if user is None:
            return False

        await db.delete(user)
        await db.flush()
        return True


user_service = UserService()
