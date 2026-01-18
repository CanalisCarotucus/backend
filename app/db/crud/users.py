from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.db.schema import User, UserRole
from app.core.exceptions import UserNotFound, PermissionDenied, ValidationError
from app.models.users import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserCreateWithPassport,
    UserWithPassportResponse,
    MyProfileResponse,
    MyProfileUpdate,
    AdminProfileUpdate,
)
from app.db.crud.passports import create_passport_for_user


async def _get_user_by_id_orm(db: AsyncSession, user_id: int) -> User:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise UserNotFound(f"User with id {user_id} not found")
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> UserResponse:
    user = await _get_user_by_id_orm(db, user_id)
    return UserResponse.model_validate(user)


async def get_user_by_id_with_passport(
    db: AsyncSession, user_id: int
) -> UserWithPassportResponse:
    query = select(User).where(User.id == user_id).options(selectinload(User.passport))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise UserNotFound(f"User with id {user_id} not found")
    return UserWithPassportResponse.model_validate(user)


async def get_all_users(db: AsyncSession) -> List[UserResponse]:
    result = await db.execute(select(User))
    users = list(result.scalars().all())
    return [UserResponse.model_validate(u) for u in users]


async def create_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    try:
        user_dict = user_data.model_dump()
        user = User(**user_dict)
        user_dict.pop("role", None)
        user_dict["role"] = "user"
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return UserResponse.model_validate(user)
    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)

        if "username" in error_msg.lower():
            detail = "Username already exists"
        elif "email" in error_msg.lower():
            detail = "Email already exists"
        else:
            detail = "Database constraint violation"

        raise ValidationError(detail)


async def update_user(
    db: AsyncSession, user_id: int, user_data: UserUpdate
) -> UserResponse:
    user = await _get_user_by_id_orm(db, user_id)

    update_dict = user_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)

    await db.flush()
    await db.refresh(user)
    return UserResponse.model_validate(user)


async def delete_user(db: AsyncSession, user_id: int) -> None:
    user = await _get_user_by_id_orm(db, user_id)
    await db.delete(user)
    await db.flush()


async def create_user_with_passport(
    db: AsyncSession, user_data: UserCreateWithPassport
) -> UserWithPassportResponse:
    try:
        user_dict = user_data.model_dump(exclude={"passport"})
        user_create = UserCreate(**user_dict)
        user_response = await create_user(db, user_create)

        if user_data.passport:
            passport_dict = user_data.passport.model_dump()
            await create_passport_for_user(db, user_response.id, passport_dict)

        return await get_user_by_id_with_passport(db, user_response.id)
    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)

        if "username" in error_msg.lower():
            detail = "Username already exists"
        elif "email" in error_msg.lower():
            detail = "Email already exists"
        elif "passport_number" in error_msg.lower():
            detail = "Passport number already exists"
        else:
            detail = "Database constraint violation"

        raise ValidationError(detail)


async def get_user_profile(db: AsyncSession, user_id: int) -> MyProfileResponse:
    user = await _get_user_by_id_orm(db, user_id)
    return MyProfileResponse.model_validate(user)


async def update_user_profile(
    db: AsyncSession, user_id: int, profile_data: MyProfileUpdate
) -> MyProfileResponse:
    user = await _get_user_by_id_orm(db, user_id)

    update_dict = profile_data.model_dump(exclude_unset=True)
    allowed_fields = {"username", "email"}
    filtered_dict = {k: v for k, v in update_dict.items() if k in allowed_fields}

    if len(filtered_dict) != len(update_dict):
        raise ValidationError("You can only update username and email")

    for key, value in filtered_dict.items():
        setattr(user, key, value)

    await db.flush()
    await db.refresh(user)
    return MyProfileResponse.model_validate(user)


async def update_user_profile_admin(
    db: AsyncSession, user_id: int, profile_data: AdminProfileUpdate
) -> MyProfileResponse:
    user = await _get_user_by_id_orm(db, user_id)

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

    await db.flush()
    await db.refresh(user)
    return MyProfileResponse.model_validate(user)
