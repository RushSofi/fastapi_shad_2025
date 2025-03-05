from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.sellers import Seller
from src.schemas import (
    IncomingSeller,
    ReturnedSeller,
    ReturnedAllSellers,
    UpdateSeller,
)
from src.configurations import get_async_session

sellers_router = APIRouter(tags=["sellers"], prefix="/seller")


# Регистрация продавца
@sellers_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(
    seller: IncomingSeller,
    session: AsyncSession = Depends(get_async_session),
):
    new_seller = Seller(**seller.model_dump())
    session.add(new_seller)
    await session.flush()
    return new_seller


# Получение списка продавцов
@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Seller))
    sellers = result.scalars().all()
    return {"sellers": sellers}


# Получение данных о конкретном продавце
@sellers_router.get("/{seller_id}", response_model=ReturnedSeller)
async def get_seller(seller_id: int, session: AsyncSession = Depends(get_async_session)):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    return seller


# Обновление данных продавца
@sellers_router.put("/{seller_id}", response_model=ReturnedSeller)
async def update_seller(
    seller_id: int,
    new_data: UpdateSeller,
    session: AsyncSession = Depends(get_async_session),
):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    # Обновляем только те поля, которые переданы в запросе
    if new_data.first_name is not None:
        seller.first_name = new_data.first_name
    if new_data.last_name is not None:
        seller.last_name = new_data.last_name
    if new_data.e_mail is not None:
        seller.e_mail = new_data.e_mail
    if new_data.password is not None:
        seller.password = new_data.password

    await session.flush()
    return seller


# Удаление продавца
@sellers_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: AsyncSession = Depends(get_async_session)):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    await session.delete(seller)
    await session.flush()