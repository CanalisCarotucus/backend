from fastapi import APIRouter, Depends

from app.models.users import (
    UserCreate, UserUpdate, UserResponse,
    MyProfileResponse, MyProfileUpdate, AdminProfileUpdate
)
from app.models.responses import DataResponse, ListDataResponse
from app.core.dependencies import get_current_user, get_user_service
from app.services.user_service import UserService
from app.database.models import User

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/users", response_model=ListDataResponse[UserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users()
    return ListDataResponse(data=[UserResponse.model_validate(u) for u in users])


@router.get("/users/{user_id}", response_model=DataResponse[UserResponse])
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user(user_id)
    return DataResponse(data=UserResponse.model_validate(user))


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create_user(user_data.model_dump())
    return UserResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    update_dict = user_data.model_dump(exclude_unset=True)
    user = await user_service.update_user(user_id, update_dict)
    return UserResponse.model_validate(user)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    success = await user_service.delete_user(user_id)
    if not success:
        from app.core.exceptions import UserNotFound
        raise UserNotFound(f"User with id {user_id} not found")


@router.get("/myprofile", response_model=DataResponse[MyProfileResponse])
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return DataResponse(data=MyProfileResponse.model_validate(current_user))


@router.put("/myprofile", response_model=MyProfileResponse)
async def update_my_profile(
    profile_data: MyProfileUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    update_dict = profile_data.model_dump(exclude_unset=True)
    updated_user = await user_service.update_my_profile(current_user.id, update_dict)
    return MyProfileResponse.model_validate(updated_user)


@router.put("/myprofile/admin", response_model=MyProfileResponse)
async def update_my_profile_admin(
    profile_data: AdminProfileUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    update_dict = profile_data.model_dump(exclude_unset=True)
    updated_user = await user_service.update_my_profile_admin(current_user.id, update_dict)
    return MyProfileResponse.model_validate(updated_user)
