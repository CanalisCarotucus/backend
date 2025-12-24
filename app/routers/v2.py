from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.users import UserCreateWithPassport, UserUpdate, UserWithPassportResponse
from app.models.responses import DataResponse
from app.database.connection import get_db
from app.core.dependencies import get_user_service
from app.services.user_service import UserService
from app.core.exceptions import ValidationError

router = APIRouter(prefix="/api/v2", tags=["v2"])


@router.get("/users/{user_id}", response_model=DataResponse[UserWithPassportResponse])
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user_with_passport(user_id)
    return DataResponse(data=UserWithPassportResponse.model_validate(user))


@router.post("/users", response_model=UserWithPassportResponse, status_code=201)
async def create_user(
    user_data: UserCreateWithPassport,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    user_dict = {"first_name": user_data.first_name, "last_name": user_data.last_name}

    try:
        if user_data.passport:
            passport_dict = {
                "passport_number": user_data.passport.passport_number,
                "city": user_data.passport.city,
            }
            user = await user_service.create_user_with_passport(user_dict, passport_dict)
        else:
            user = await user_service.create_user(user_dict)

        user_with_passport = await user_service.get_user_with_passport(user.id)
        return UserWithPassportResponse.model_validate(user_with_passport)

    except IntegrityError:
        await db.rollback()
        raise ValidationError("Duplicate passport number or constraint violation")


@router.put("/users/{user_id}", response_model=UserWithPassportResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    update_dict = user_data.model_dump(exclude_unset=True)
    user = await user_service.update_user(user_id, update_dict)
    user_with_passport = await user_service.get_user_with_passport(user_id)
    return UserWithPassportResponse.model_validate(user_with_passport)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    success = await user_service.delete_user(user_id)
    if not success:
        from app.core.exceptions import UserNotFound
        raise UserNotFound(f"User with id {user_id} not found")
