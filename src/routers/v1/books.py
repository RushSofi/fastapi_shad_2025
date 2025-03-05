from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.books import Book
from src.schemas import (
    IncomingBook,
    ReturnedBook,
    ReturnedAllbooks,
    UpdateBook,
)
from src.configurations import get_async_session

books_router = APIRouter(tags=["books"], prefix="/books")


# Ручка для создания книги
@books_router.post("/", response_model=ReturnedBook, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: IncomingBook,
    session: AsyncSession = Depends(get_async_session),
):
    new_book = Book(**book.model_dump())
    session.add(new_book)
    await session.flush()
    return new_book


# Ручка для получения списка книг
@books_router.get("/", response_model=ReturnedAllbooks)
async def get_all_books(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    return {"books": books}


# Ручка для получения книги по ее ИД
@books_router.get("/{book_id}", response_model=ReturnedBook)
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


# Ручка для обновления данных книги
@books_router.put("/{book_id}", response_model=ReturnedBook)
async def update_book(
    book_id: int,
    new_data: UpdateBook,
    session: AsyncSession = Depends(get_async_session),
):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # Обновляем только те поля, которые переданы в запросе
    if new_data.title is not None:
        book.title = new_data.title
    if new_data.author is not None:
        book.author = new_data.author
    if new_data.year is not None:
        book.year = new_data.year
    if new_data.pages is not None:
        book.pages = new_data.pages
    if new_data.seller_id is not None:
        book.seller_id = new_data.seller_id

    await session.flush()
    return book


# Ручка для удаления книги
@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    await session.delete(book)
    await session.flush()
