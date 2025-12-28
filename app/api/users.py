from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_db
from app.crud.users import UserCRUD
from app.schemas.users import (
    UserCreate, UserUpdate, UserResponse, UserCreateWithPassport,
    UserWithPassportResponse, MyProfileResponse, MyProfileUpdate,
    AdminProfileUpdate
)
from app.schemas.responses import DataResponse, ListDataResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=ListDataResponse[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    user_crud = UserCRUD(db)
    users = await user_crud.get_all()
    return ListDataResponse(data=users)


@router.get("/{user_id}", response_model=DataResponse[UserResponse])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_crud = UserCRUD(db)
    user = await user_crud.get_by_id(user_id)
    return DataResponse(data=user)


@router.post("", response_model=DataResponse[UserResponse], status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_crud = UserCRUD(db)
    user = await user_crud.create(user_data)
    return DataResponse(data=user)


@router.put("/{user_id}", response_model=DataResponse[UserResponse])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user_crud = UserCRUD(db)
    user = await user_crud.update(user_id, user_data)
    return DataResponse(data=user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_crud = UserCRUD(db)
    await user_crud.delete(user_id)


@router.get("/{user_id}/with-passport", response_model=DataResponse[UserWithPassportResponse])
async def get_user_with_passport(user_id: int, db: AsyncSession = Depends(get_db)):
    user_crud = UserCRUD(db)
    user = await user_crud.get_by_id_with_passport(user_id)
    return DataResponse(data=user)


@router.post("/with-passport", response_model=DataResponse[UserWithPassportResponse], status_code=201)
async def create_user_with_passport(
    user_data: UserCreateWithPassport,
    db: AsyncSession = Depends(get_db)
):
    user_crud = UserCRUD(db)
    user = await user_crud.create_with_passport(user_data)
    return DataResponse(data=user)


@router.get("/{user_id}/profile", response_model=DataResponse[MyProfileResponse])
async def get_my_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    user_crud = UserCRUD(db)
    user = await user_crud.get_profile(user_id)
    return DataResponse(data=user)


@router.put("/{user_id}/profile", response_model=DataResponse[MyProfileResponse])
async def update_my_profile(
    user_id: int,
    profile_data: MyProfileUpdate,
    db: AsyncSession = Depends(get_db)
):
    user_crud = UserCRUD(db)
    updated_user = await user_crud.update_profile(user_id, profile_data)
    return DataResponse(data=updated_user)


@router.put("/{user_id}/profile/admin", response_model=DataResponse[MyProfileResponse])
async def update_my_profile_admin(
    user_id: int,
    profile_data: AdminProfileUpdate,
    db: AsyncSession = Depends(get_db)
):
    user_crud = UserCRUD(db)
    updated_user = await user_crud.update_profile_admin(user_id, profile_data)
    return DataResponse(data=updated_user)
