import pytest
from fastapi import status
from sqlalchemy import select
from src.models.books import Book
from src.models.sellers import Seller


@pytest.mark.asyncio
async def test_create_book(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    data = {
        "title": "Clean Architecture",
        "author": "Robert Martin",
        "count_pages": 300,
        "year": 2025,
        "seller_id": seller.id,
    }
    response = await async_client.post("/api/v1/books/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    result_data = response.json()
    assert result_data["title"] == "Clean Architecture"
    assert result_data["author"] == "Robert Martin"


@pytest.mark.asyncio
async def test_get_all_books(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="Clean Architecture",
        author="Robert Martin",
        year=2025,
        pages=300,
        seller_id=seller.id,
    )
    db_session.add(book)
    await db_session.flush()

    response = await async_client.get("/api/v1/books/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["books"]) == 1


@pytest.mark.asyncio
async def test_get_single_book(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="Clean Architecture",
        author="Robert Martin",
        year=2025,
        pages=300,
        seller_id=seller.id,
    )
    db_session.add(book)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/books/{book.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Clean Architecture"


@pytest.mark.asyncio
async def test_update_book(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="Clean Architecture",
        author="Robert Martin",
        year=2025,
        pages=300,
        seller_id=seller.id,
    )
    db_session.add(book)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/books/{book.id}",
        json={
            "title": "Clean Code",
            "author": "Robert Martin",
            "count_pages": 310,
            "year": 2022,
            "seller_id": seller.id,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Clean Code"


@pytest.mark.asyncio
async def test_delete_book(async_client, db_session):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="password123",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="Clean Architecture",
        author="Robert Martin",
        year=2025,
        pages=300,
        seller_id=seller.id,
    )
    db_session.add(book)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/books/{book.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.get(f"/api/v1/books/{book.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    