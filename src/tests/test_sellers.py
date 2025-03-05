import pytest
from fastapi import status
from src.models.sellers import Seller


@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john.doe@example.com",
        "password": "password123",
    }
    response = await async_client.post("/api/v1/seller/", json=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_all_sellers(async_client):
    response = await async_client.get("/api/v1/seller/")
    assert response.status_code == status.HTTP_200_OK