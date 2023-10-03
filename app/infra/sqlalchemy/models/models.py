from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey

from ..config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30))
    password = Column(String(200))
    username = Column(String(30))
    name = Column(String(30))
    telephone = Column(String(30))
    sex = Column(String(10))
    birth_date = Column(Date)


class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    description = Column(String(100))
    price = Column(Integer)
