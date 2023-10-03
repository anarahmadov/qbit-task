from datetime import date
import uuid
from pydantic import BaseModel
from typing import Optional, List


# standart user
class User(BaseModel):
    id: int
    email: str
    password: str
    username: str
    name: str
    telephone: str
    sex: str
    birth_date: date

    class Config:
        orm_mode = True


# user try to login
class TryLoginUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


# logged in user
class LoggedUser(BaseModel):
    id: int
    email: str
    password: str
    name: str
    username: str
    telephone: str
    sex: str
    birth_date: date
    token_id: str


# login user
class LoginUser(BaseModel):
    id: int
    password: str


class Listing(BaseModel):
    id: int
    name: str
    description: str
    price: int
