from pydantic import BaseModel, EmailStr, Field
from typing import Optional  

__all__ = ["BaseSeller", "IncomingSeller", "ReturnedSeller", "ReturnedAllSellers", "UpdateSeller"]

class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr


class IncomingSeller(BaseSeller):
    password: str = Field(min_length=6)


class ReturnedSeller(BaseSeller):
    id: int


class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]


class UpdateSeller(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
