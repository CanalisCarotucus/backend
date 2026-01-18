from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_db
from app.db.crud.users import (
    get_all_users as get_all_users_crud,
    get_user_by_id as get_user_by_id_crud,
    create_user as create_user_crud,
    update_user as update_user_crud,
    delete_user as delete_user_crud,
    get_user_by_id_with_passport as get_user_by_id_with_passport_crud,
    create_user_with_passport as create_user_with_passport_crud,
    get_user_profile as get_user_profile_crud,
    update_user_profile as update_user_profile_crud,
    update_user_profile_admin as update_user_profile_admin_crud,
)
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
from app.models.responses import DataResponse, ListDataResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=ListDataResponse[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users_crud(db)
    return ListDataResponse(data=users)


@router.get("/{user_id}", response_model=DataResponse[UserResponse])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id_crud(db, user_id)
    return DataResponse(data=user)


@router.post("", response_model=DataResponse[UserResponse], status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user_crud(db, user_data)
    return DataResponse(data=user)


@router.put("/{user_id}", response_model=DataResponse[UserResponse])
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    user = await update_user_crud(db, user_id, user_data)
    return DataResponse(data=user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_user_crud(db, user_id)


@router.get(
    "/{user_id}/with-passport", response_model=DataResponse[UserWithPassportResponse]
)
async def get_user_with_passport(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id_with_passport_crud(db, user_id)
    return DataResponse(data=user)


@router.post(
    "/with-passport",
    response_model=DataResponse[UserWithPassportResponse],
    status_code=201,
)
async def create_user_with_passport(
    user_data: UserCreateWithPassport, db: AsyncSession = Depends(get_db)
):
    user = await create_user_with_passport_crud(db, user_data)
    return DataResponse(data=user)


@router.get("/{user_id}/profile", response_model=DataResponse[MyProfileResponse])
async def get_my_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_profile_crud(db, user_id)
    return DataResponse(data=user)


@router.put("/{user_id}/profile", response_model=DataResponse[MyProfileResponse])
async def update_my_profile(
    user_id: int, profile_data: MyProfileUpdate, db: AsyncSession = Depends(get_db)
):
    updated_user = await update_user_profile_crud(db, user_id, profile_data)
    return DataResponse(data=updated_user)


@router.put("/{user_id}/profile/admin", response_model=DataResponse[MyProfileResponse])
async def update_my_profile_admin(
    user_id: int, profile_data: AdminProfileUpdate, db: AsyncSession = Depends(get_db)
):
    updated_user = await update_user_profile_admin_crud(db, user_id, profile_data)
    return DataResponse(data=updated_user)
