from fastapi import Depends, HTTPException, status, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.connection import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.passport_repository import PassportRepository
from app.services.user_service import UserService
from app.services.passport_service import PassportService
from app.database.models import User
from app.core.exceptions import UserNotFound


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_passport_repository(db: AsyncSession = Depends(get_db)) -> PassportRepository:
    return PassportRepository(db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    passport_repository: PassportRepository = Depends(get_passport_repository)
) -> UserService:
    return UserService(user_repository, passport_repository)


def get_passport_service(
    passport_repository: PassportRepository = Depends(get_passport_repository),
    user_repository: UserRepository = Depends(get_user_repository)
) -> PassportService:
    return PassportService(passport_repository, user_repository)


async def get_current_user(
    x_user_id: Optional[int] = Header(None, alias="X-User-ID"),
    user_id: Optional[int] = Query(None),
    user_service: UserService = Depends(get_user_service)
) -> User:
    current_user_id = x_user_id or user_id
    if current_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required. Provide X-User-ID header or user_id query parameter."
        )
    
    try:
        return await user_service.get_user(current_user_id)
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

