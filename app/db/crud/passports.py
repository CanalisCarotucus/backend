from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.schema import Passport, User
from app.core.exceptions import UserNotFound, PassportNotFound, PassportAlreadyExists
from app.models.passports import (
    PassportCreate,
    PassportCreateWithUser,
    PassportUpdate,
    PassportResponse,
)


async def _get_passport_by_id_orm(db: AsyncSession, passport_id: int) -> Passport:
    query = select(Passport).where(Passport.id == passport_id)
    result = await db.execute(query)
    passport = result.scalar_one_or_none()
    if passport is None:
        raise PassportNotFound(f"Passport with id {passport_id} not found")
    return passport


async def get_passport_by_id(db: AsyncSession, passport_id: int) -> PassportResponse:
    passport = await _get_passport_by_id_orm(db, passport_id)
    return PassportResponse.model_validate(passport)


async def get_passport_by_user_id(
    db: AsyncSession, user_id: int
) -> Optional[PassportResponse]:
    query = select(Passport).where(Passport.user_id == user_id)
    result = await db.execute(query)
    passport = result.scalar_one_or_none()
    if passport is None:
        return None
    return PassportResponse.model_validate(passport)


async def _get_passport_by_user_id_orm(
    db: AsyncSession, user_id: int
) -> Optional[Passport]:
    query = select(Passport).where(Passport.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_all_passports(db: AsyncSession) -> List[PassportResponse]:
    result = await db.execute(select(Passport))
    passports = list(result.scalars().all())
    return [PassportResponse.model_validate(p) for p in passports]


async def _create_passport_orm(db: AsyncSession, passport_data: dict) -> Passport:
    passport = Passport(**passport_data)
    db.add(passport)
    await db.flush()
    await db.refresh(passport)
    return passport


async def create_passport(
    db: AsyncSession, passport_data: PassportCreate
) -> PassportResponse:
    passport_dict = passport_data.model_dump()
    passport = await _create_passport_orm(db, passport_dict)
    return PassportResponse.model_validate(passport)


async def update_passport(
    db: AsyncSession, passport_id: int, passport_data: PassportUpdate
) -> PassportResponse:
    passport = await _get_passport_by_id_orm(db, passport_id)

    update_dict = passport_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(passport, key, value)

    await db.flush()
    await db.refresh(passport)
    return PassportResponse.model_validate(passport)


async def delete_passport(db: AsyncSession, passport_id: int) -> None:
    passport = await _get_passport_by_id_orm(db, passport_id)
    await db.delete(passport)
    await db.flush()


async def create_passport_for_user(
    db: AsyncSession, user_id: int, passport_data: dict
) -> Passport:
    user_query = select(User).where(User.id == user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()
    if user is None:
        raise UserNotFound(f"User with id {user_id} not found")

    existing = await _get_passport_by_user_id_orm(db, user_id)
    if existing:
        raise PassportAlreadyExists(f"User with id {user_id} already has a passport")

    passport_data["user_id"] = user_id
    return await _create_passport_orm(db, passport_data)


async def create_passport_for_user_from_schema(
    db: AsyncSession, passport_data: PassportCreateWithUser
) -> PassportResponse:
    passport_dict = passport_data.model_dump(exclude={"user_id"})
    passport_orm = await create_passport_for_user(
        db, passport_data.user_id, passport_dict
    )
    return PassportResponse.model_validate(passport_orm)
