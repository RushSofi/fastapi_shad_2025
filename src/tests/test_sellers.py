import pytest
from fastapi import status
from sqlalchemy import select
from src.models.sellers import Seller
from src.schemas import ReturnedSeller, ReturnedAllSellers


@pytest.mark.asyncio
async def test_create_seller(async_client, db_session):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john.doe@example.com",
        "password": "password123",
    }
    response = await async_client.post("/api/v1/seller/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    result_data = response.json()
    assert result_data["first_name"] == "John"
    assert result_data["last_name"] == "Doe"
    assert result_data["e_mail"] == "john.doe@example.com"


@pytest.mark.asyncio
async def test_get_all_sellers(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["sellers"]) == 1


@pytest.mark.asyncio
async def test_get_single_seller(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "John"


@pytest.mark.asyncio
async def test_update_seller(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/seller/{seller.id}",
        json={
            "first_name": "John",
            "last_name": "Smith",
            "e_mail": "john.smith@example.com",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["last_name"] == "Smith"


@pytest.mark.asyncio
async def test_delete_seller(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{seller.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.get(f"/api/v1/seller/{seller.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    