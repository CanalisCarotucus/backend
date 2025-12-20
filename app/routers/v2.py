from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.users import UserCreateWithPassport, UserUpdate, UserWithPassportResponse
from app.database.connection import get_db
from app.services import user_service
from app.exceptions import UserNotFound, PassportAlreadyExists

router = APIRouter(prefix="/api/v2", tags=["v2"])


@router.get("/users/{user_id}", response_model=UserWithPassportResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user_with_passport(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return UserWithPassportResponse.model_validate(user)


@router.post("/users", response_model=UserWithPassportResponse, status_code=201)
async def create_user(user_data: UserCreateWithPassport, db: AsyncSession = Depends(get_db)):
    user_dict = {"first_name": user_data.first_name, "last_name": user_data.last_name}

    try:
        if user_data.passport:
            passport_dict = {
                "passport_number": user_data.passport.passport_number,
                "city": user_data.passport.city,
            }
            user = await user_service.create_user_with_passport(db, user_dict, passport_dict)
        else:
            user = await user_service.create_user(db, user_dict)

        user_with_passport = await user_service.get_user_with_passport(db, user.id)
        if user_with_passport:
            user = user_with_passport

        return UserWithPassportResponse.model_validate(user)

    except (UserNotFound, PassportAlreadyExists) as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Duplicate passport number or constraint violation"
        )


@router.put("/users/{user_id}", response_model=UserWithPassportResponse)
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    update_dict = user_data.model_dump(exclude_unset=True)
    user = await user_service.update_user(db, user_id, update_dict)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    user_with_passport = await user_service.get_user_with_passport(db, user_id)
    return UserWithPassportResponse.model_validate(user_with_passport)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
