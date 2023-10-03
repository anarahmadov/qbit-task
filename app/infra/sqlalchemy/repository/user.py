from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends

from app.infra.sqlalchemy.config.database import get_db
from ..models import models
from ....schemas import schemas


class ReposityUser:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, user: schemas.User):
        db_user = models.User(
            id=user.id,
            email=user.email,
            password=user.password,
            name=user.name,
            username=user.username,
            telephone=user.telephone,
            sex=user.sex,
            birth_date=user.birth_date,
        )
        self.db.add(db_user)
        self.db.commit()
        # self.db.refresh(db_user)
        return db_user

    def list_all(self):
        statement = select(models.User)
        users = self.db.execute(statement).scalars().all()
        return users

    def search_id(self, number: int) -> schemas.User:
        statement = select(models.User).where(models.User.id == number)
        user = self.db.execute(statement).scalars().first()
        return user
