from fastapi import APIRouter, Depends, Header
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.routers.utils import retrieve_token_from_redis, if_token_exists_then_update
from ..schemas import schemas
from ..infra.sqlalchemy.config import database
from ..infra.sqlalchemy.repository import listing


router = APIRouter()


# -- listings -- #


# create listing
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_listing(
    data: schemas.Listing,
    token_id: str = Header(),
    db: Session = Depends(database.get_db),
):
    if token_id:
        # Update the user's activity timestamp in Redis
        exists = if_token_exists_then_update(token_id)
        # if there is no such token return unauthorized response
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg": "Login expired"},
            )

    listing_by_id = listing.ReposityListing(db).get_listing_by_id(data.id)

    if listing_by_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": "Listing already registered!"},
        )

    return listing.ReposityListing(db).create(data)


# edit listing
@router.put("/edit", status_code=status.HTTP_200_OK)
def edit_listing(
    data: schemas.Listing,
    token_id: str = Header(),
    db: Session = Depends(database.get_db),
):
    if token_id:
        # Update the user's activity timestamp in Redis
        exists = if_token_exists_then_update(token_id)
        # if there is no such token return unauthorized response
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg": "Login expired"},
            )

    listing_by_id = listing.ReposityListing(db).get_listing_by_id(data.id)

    if not listing_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Not found such listing"},
        )

    return listing.ReposityListing(db).edit(data)


# filter listing by price
@router.get("/filter", status_code=status.HTTP_200_OK)
def filter_listing(token_id: str = Header(), db: Session = Depends(database.get_db)):
    if token_id:
        # Update the user's activity timestamp in Redis
        exists = if_token_exists_then_update(token_id)
        print(exists)
        # if there is such no token return unauthorized response
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg": "Login expired"},
            )

    all_listings = listing.ReposityListing(
        db
    ).list_all_listings_by_price_between_100_and_1000()

    if not all_listings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Not found such listing"},
        )

    return all_listings
