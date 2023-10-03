import json
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.routers.utils import save_token_on_redis
from app.schemas import schemas
from ..infra.providers import hash
from ..infra.sqlalchemy.config import database
from ..infra.sqlalchemy.repository import user
from ..infra.providers.token import create_jwt_token
from ..infra.sqlalchemy.config.database import get_db


router = APIRouter()


# -- users -- #


# register
@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.TryLoginUser
)
def signup(data: schemas.User, db: Session = Depends(get_db)):
    data.password = hash.make_hash(data.password)

    if user.ReposityUser(db).search_id(data.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": "User already registered!"},
        )

    return user.ReposityUser(db).create(data)


# login
@router.post("/signin", response_model=schemas.LoggedUser)
def signin(user_data: schemas.LoginUser, db: Session = Depends(get_db)):
    # get user entity from DB
    userEntity = user.ReposityUser(db).search_id(user_data.id)
    print(userEntity)
    print(user_data)
    # check if user exists
    if not userEntity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "User not found"},
        )

    # check if user type correct password or not
    if not hash.verify_hash(user_data.password, userEntity.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Wrong password"},
        )

    # make a initial token
    initial_jwt_info = create_jwt_token({"sub": user_data.id})

    # store the token on Redis
    save_token_on_redis(initial_jwt_info["token_id"], initial_jwt_info["token"])

    return schemas.LoggedUser(
        id=userEntity.id,
        email=userEntity.email,
        password=userEntity.password,
        username=userEntity.username,
        name=userEntity.name,
        telephone=userEntity.telephone,
        sex=userEntity.sex,
        birth_date=userEntity.birth_date,
        token_id=initial_jwt_info["token_id"],
    )
