from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.passport_repository import PassportRepository
from app.repositories.user_repository import UserRepository
from app.database.models import Passport
from app.core.exceptions import UserNotFound, PassportNotFound, PassportAlreadyExists


class PassportService:
    def __init__(
        self,
        passport_repository: PassportRepository,
        user_repository: UserRepository
    ):
        self.passport_repository = passport_repository
        self.user_repository = user_repository

    async def get_passport(self, passport_id: int) -> Passport:
        passport = await self.passport_repository.get_by_id(passport_id)
        if passport is None:
            raise PassportNotFound(f"Passport with id {passport_id} not found")
        return passport

    async def get_passport_by_user_id(self, user_id: int) -> Optional[Passport]:
        return await self.passport_repository.get_by_user_id(user_id)

    async def create_passport_for_user(
        self, user_id: int, passport_data: dict
    ) -> Passport:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")

        existing = await self.passport_repository.get_by_user_id(user_id)
        if existing:
            raise PassportAlreadyExists(f"User with id {user_id} already has a passport")

        passport_data["user_id"] = user_id
        return await self.passport_repository.create(passport_data)

    async def update_passport(self, passport_id: int, passport_data: dict) -> Passport:
        passport = await self.passport_repository.update(passport_id, passport_data)
        if passport is None:
            raise PassportNotFound(f"Passport with id {passport_id} not found")
        return passport

    async def delete_passport(self, passport_id: int) -> bool:
        return await self.passport_repository.delete(passport_id)
