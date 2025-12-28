from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_db
from app.crud.passports import PassportCRUD
from app.schemas.passports import (
    PassportCreate, PassportCreateWithUser, PassportUpdate, PassportResponse
)
from app.schemas.responses import DataResponse, ListDataResponse

router = APIRouter(prefix="/api/passports", tags=["passports"])


@router.get("", response_model=ListDataResponse[PassportResponse])
async def get_all_passports(db: AsyncSession = Depends(get_db)):
    passport_crud = PassportCRUD(db)
    passports = await passport_crud.get_all()
    return ListDataResponse(data=passports)


@router.get("/{passport_id}", response_model=DataResponse[PassportResponse])
async def get_passport(passport_id: int, db: AsyncSession = Depends(get_db)):
    passport_crud = PassportCRUD(db)
    passport = await passport_crud.get_by_id(passport_id)
    return DataResponse(data=passport)


@router.get("/user/{user_id}", response_model=DataResponse[PassportResponse])
async def get_passport_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    passport_crud = PassportCRUD(db)
    passport = await passport_crud.get_by_user_id(user_id)
    if passport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Passport for user with id {user_id} not found"
        )
    return DataResponse(data=passport)


@router.post("", response_model=DataResponse[PassportResponse], status_code=201)
async def create_passport(passport_data: PassportCreateWithUser, db: AsyncSession = Depends(get_db)):
    passport_crud = PassportCRUD(db)
    passport = await passport_crud.create_for_user_from_schema(passport_data)
    return DataResponse(data=passport)


@router.put("/{passport_id}", response_model=DataResponse[PassportResponse])
async def update_passport(
    passport_id: int,
    passport_data: PassportUpdate,
    db: AsyncSession = Depends(get_db)
):
    passport_crud = PassportCRUD(db)
    passport = await passport_crud.update(passport_id, passport_data)
    return DataResponse(data=passport)


@router.delete("/{passport_id}", status_code=204)
async def delete_passport(passport_id: int, db: AsyncSession = Depends(get_db)):
    passport_crud = PassportCRUD(db)
    await passport_crud.delete(passport_id)
