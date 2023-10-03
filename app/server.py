from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.exception import ExceptionHandlerMiddleware
from .infra.sqlalchemy.config import database
from .routers import users, listings
from .middlewares.inactive_token_expiration import InactiveTokenExpiration

# uvicorn mercadoGamer-backend.server:app --reload --reload-dir=mercadoGamer-backend
database.create_db()
app = FastAPI()


# InactiveTokenExpiration middle
# app.add_middleware(InactiveTokenExpiration)


# Error handling middle
# app.add_middleware(ExceptionHandlerMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTERS
app.include_router(users.router, prefix="/user", tags=["users"])
app.include_router(listings.router, prefix="/listing", tags=["listings"])
