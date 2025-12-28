from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.db.models import User, UserRole
from app.core.exceptions import UserNotFound, PermissionDenied, ValidationError
from app.schemas.users import (
    UserCreate, UserUpdate, UserResponse, UserCreateWithPassport,
    UserWithPassportResponse, MyProfileResponse, MyProfileUpdate,
    AdminProfileUpdate
)
from app.crud.passports import PassportCRUD


class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_by_id_orm(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")
        return user

    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self._get_by_id_orm(user_id)
        return UserResponse.model_validate(user)

    async def get_by_id_with_passport(self, user_id: int) -> UserWithPassportResponse:
        query = select(User).where(User.id == user_id).options(
            selectinload(User.passport)
        )
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFound(f"User with id {user_id} not found")
        return UserWithPassportResponse.model_validate(user)

    async def get_all(self) -> List[UserResponse]:
        result = await self.db.execute(select(User))
        users = list(result.scalars().all())
        return [UserResponse.model_validate(u) for u in users]

    async def create(self, user_data: UserCreate) -> UserResponse:
        user_dict = user_data.model_dump()
        user = User(**user_dict)
        user_dict.pop('role', None)
        user_dict['role'] = "user"
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return UserResponse.model_validate(user)

    async def update(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = await self._get_by_id_orm(user_id)
        
        update_dict = user_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(user, key, value)

        await self.db.flush()
        await self.db.refresh(user)
        return UserResponse.model_validate(user)

    async def delete(self, user_id: int) -> None:
        user = await self._get_by_id_orm(user_id)
        await self.db.delete(user)
        await self.db.flush()

    async def create_with_passport(
        self, user_data: UserCreateWithPassport
    ) -> UserWithPassportResponse:
        try:
            user_dict = user_data.model_dump(exclude={"passport"})
            user_create = UserCreate(**user_dict)
            user_response = await self.create(user_create)
            
            if user_data.passport:
                passport_crud = PassportCRUD(self.db)
                passport_dict = user_data.passport.model_dump()
                await passport_crud.create_for_user(user_response.id, passport_dict)
            
            return await self.get_by_id_with_passport(user_response.id)
        except IntegrityError as e:
            await self.db.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            
            if "username" in error_msg.lower():
                detail = "Username already exists"
            elif "email" in error_msg.lower():
                detail = "Email already exists"
            elif "passport_number" in error_msg.lower():
                detail = "Passport number already exists"
            else:
                detail = "Database constraint violation"
            
            raise ValidationError(detail)

    async def get_profile(self, user_id: int) -> MyProfileResponse:
        user = await self._get_by_id_orm(user_id)
        return MyProfileResponse.model_validate(user)

    async def update_profile(
        self, user_id: int, profile_data: MyProfileUpdate
    ) -> MyProfileResponse:
        user = await self._get_by_id_orm(user_id)

        update_dict = profile_data.model_dump(exclude_unset=True)
        allowed_fields = {"username", "email"}
        filtered_dict = {k: v for k, v in update_dict.items() if k in allowed_fields}
        
        if len(filtered_dict) != len(update_dict):
            raise ValidationError("You can only update username and email")
        
        for key, value in filtered_dict.items():
            setattr(user, key, value)

        await self.db.flush()
        await self.db.refresh(user)
        return MyProfileResponse.model_validate(user)

    async def update_profile_admin(
        self, user_id: int, profile_data: AdminProfileUpdate
    ) -> MyProfileResponse:
        user = await self._get_by_id_orm(user_id)

        if user.role != UserRole.ADMIN:
            raise PermissionDenied("Only administrators can use this endpoint")
        
        update_dict = profile_data.model_dump(exclude_unset=True)
        if "role" in update_dict:
            try:
                update_dict["role"] = UserRole(update_dict["role"])
            except ValueError:
                raise ValidationError("Invalid role. Must be 'user' or 'admin'")
        
        for key, value in update_dict.items():
            setattr(user, key, value)

        await self.db.flush()
        await self.db.refresh(user)
        return MyProfileResponse.model_validate(user)
