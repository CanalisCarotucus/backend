from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserCreate, UserUpdate, UserResponse, UsersListResponse
from app.database.connection import get_db
from app.services import user_service

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/users", response_model=UsersListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(db)
    return UsersListResponse(users=[UserResponse.model_validate(u) for u in users])


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return UserResponse.model_validate(user)


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await user_service.create_user(db, user_data.model_dump())
    return UserResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    update_dict = user_data.model_dump(exclude_unset=True)
    user = await user_service.update_user(db, user_id, update_dict)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return UserResponse.model_validate(user)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
