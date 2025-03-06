from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from typing import Optional 

__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllbooks", "UpdateBook"]


# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseBook(BaseModel):
    title: str
    author: str
    year: int
    seller_id: int


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingBook(BaseBook):
    pages: int = Field(
        default=150, alias="count_pages"
    )  # Пример использования тонкой настройки полей. Передачи в них метаинформации.

    @field_validator("year")  # Валидатор, проверяет что дата не слишком древняя
    @staticmethod
    def validate_year(val: int):
        if val < 2020:
            raise PydanticCustomError("Validation error", "Year is too old!")

        return val


# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedBook(BaseBook):
    id: int
    pages: int


# Класс для возврата массива объектов "Книга"
class ReturnedAllbooks(BaseModel):
    books: list[ReturnedBook]


# Класс для обновления данных книги
class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    pages: Optional[int] = Field(None, alias="count_pages")  # Учитываем alias
    seller_id: Optional[int] = None

    @field_validator("year")  # Валидатор для года
    @staticmethod
    def validate_year(val: Optional[int]):
        if val is not None and val < 2020:
            raise PydanticCustomError("Validation error", "Year is too old!")
        return val
    