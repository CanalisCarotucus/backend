from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_db
from app.db.crud.passports import (
    get_all_passports as get_all_passports_crud,
    get_passport_by_id as get_passport_by_id_crud,
    get_passport_by_user_id as get_passport_by_user_id_crud,
    create_passport_for_user_from_schema as create_passport_for_user_from_schema_crud,
    update_passport as update_passport_crud,
    delete_passport as delete_passport_crud,
)
from app.models.passports import (
    PassportCreateWithUser,
    PassportUpdate,
    PassportResponse,
)
from app.models.responses import DataResponse, ListDataResponse

router = APIRouter(prefix="/api/passports", tags=["passports"])


@router.get("", response_model=ListDataResponse[PassportResponse])
async def get_all_passports(db: AsyncSession = Depends(get_db)):
    passports = await get_all_passports_crud(db)
    return ListDataResponse(data=passports)


@router.get("/{passport_id}", response_model=DataResponse[PassportResponse])
async def get_passport(passport_id: int, db: AsyncSession = Depends(get_db)):
    passport = await get_passport_by_id_crud(db, passport_id)
    return DataResponse(data=passport)


@router.get("/user/{user_id}", response_model=DataResponse[PassportResponse])
async def get_passport_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    passport = await get_passport_by_user_id_crud(db, user_id)
    if passport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Passport for user with id {user_id} not found",
        )
    return DataResponse(data=passport)


@router.post("", response_model=DataResponse[PassportResponse], status_code=201)
async def create_passport(
    passport_data: PassportCreateWithUser, db: AsyncSession = Depends(get_db)
):
    passport = await create_passport_for_user_from_schema_crud(db, passport_data)
    return DataResponse(data=passport)


@router.put("/{passport_id}", response_model=DataResponse[PassportResponse])
async def update_passport(
    passport_id: int, passport_data: PassportUpdate, db: AsyncSession = Depends(get_db)
):
    passport = await update_passport_crud(db, passport_id, passport_data)
    return DataResponse(data=passport)


@router.delete("/{passport_id}", status_code=204)
async def delete_passport(passport_id: int, db: AsyncSession = Depends(get_db)):
    await delete_passport_crud(db, passport_id)
