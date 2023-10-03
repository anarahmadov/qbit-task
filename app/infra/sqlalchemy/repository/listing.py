from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.infra.sqlalchemy.config.database import SessionLocal, get_db
from ..models import models
from ....schemas import schemas
from typing import List


class ReposityListing:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_listing_by_id(self, id: int) -> schemas.Listing:
        statement = select(models.Listing).where(models.Listing.id == id)
        listing = self.db.execute(statement).scalars().first()
        return listing

    def create(self, listing: schemas.Listing):
        db_listing = models.Listing(
            id=listing.id,
            name=listing.name,
            description=listing.description,
            price=listing.price,
        )
        self.db.add(db_listing)
        self.db.commit()
        # self.db.refresh(db_listing)
        return db_listing

    def edit(self, listing: schemas.Listing):
        statement = (
            update(models.Listing)
            .where(models.Listing.id == listing.id)
            .values(
                name=listing.name,
                description=listing.description,
                price=listing.price,
            )
        )
        self.db.execute(statement)
        self.db.commit()
        # self.db.refresh()

    def list_all_listings_by_price_between_100_and_1000(self) -> List[schemas.Listing]:
        statement = select(models.Listing).where(
            models.Listing.price > 100, models.Listing.price < 1000
        )
        listings = self.db.execute(statement).scalars().all()
        return listings
