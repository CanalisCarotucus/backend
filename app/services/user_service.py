from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.repositories.passport_repository import PassportRepository
from app.database.models import User, UserRole
from app.core.exceptions import UserNotFound, PermissionDenied, ValidationError


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        passport_repository: Optional[PassportRepository] = None
    ):
        self.user_repository = user_repository
        self.passport_repository = passport_repository

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")
        return user

    async def get_user_with_passport(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id_with_passport(user_id)
        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")
        return user

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.get_all()

    async def create_user(self, user_data: dict) -> User:
        return await self.user_repository.create(user_data)

    async def create_user_with_passport(
        self, user_data: dict, passport_data: dict
    ) -> User:
        if self.passport_repository is None:
            from app.repositories.passport_repository import PassportRepository
            self.passport_repository = PassportRepository(self.user_repository.db)
        
        user = await self.user_repository.create(user_data)
        passport_data["user_id"] = user.id
        await self.passport_repository.create(passport_data)
        # Reload user with passport relationship loaded
        user = await self.user_repository.get_by_id_with_passport(user.id)
        return user

    async def update_user(self, user_id: int, user_data: dict) -> User:
        user = await self.user_repository.update(user_id, user_data)
        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")
        return user

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)

    async def update_my_profile(
        self, user_id: int, profile_data: Dict[str, Any]
    ) -> User:
        allowed_fields = {"username", "email"}
        update_dict = {k: v for k, v in profile_data.items() if k in allowed_fields}
        
        if len(update_dict) != len(profile_data):
            raise ValidationError("You can only update username and email")
        
        return await self.update_user(user_id, update_dict)

    async def update_my_profile_admin(
        self, user_id: int, profile_data: Dict[str, Any]
    ) -> User:
        user = await self.get_user(user_id)
        
        if user.role != UserRole.ADMIN:
            raise PermissionDenied("Only administrators can use this endpoint")
        
        update_dict = profile_data.copy()
        
        if "role" in update_dict:
            try:
                update_dict["role"] = UserRole(update_dict["role"])
            except ValueError:
                raise ValidationError("Invalid role. Must be 'user' or 'admin'")
        
        return await self.update_user(user_id, update_dict)
