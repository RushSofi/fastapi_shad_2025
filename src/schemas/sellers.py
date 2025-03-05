from pydantic import BaseModel, EmailStr, Field

__all__ = ["BaseSeller", "IncomingSeller", "ReturnedSeller", "ReturnedAllSellers"]

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