from datetime import datetime, timedelta
import uuid
from fastapi import Depends
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

# secret key
SECRET_KEY = "2c7f621a96d3d4b23bd2aa4ad070c9de"
# algorithm to encode
ALGORITHM = "HS256"
# Token expiration time (1 hour in this example)
TOKEN_EXPIRATION = timedelta(minutes=60)


# Function to create a JWT token with an expiration time
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + TOKEN_EXPIRATION
    to_encode.update({"exp": expire})

    token_id = str(uuid.uuid4())  # Generate a unique token ID
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"token_id": token_id, "token": token}


def encode_token(token: str):
    return jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)


def update_exp_time_of_token_itself(token: str):
    # decode the token
    decoded_token = decode_jwt_token(token)

    # update its expiration time to 1 hours from now
    decoded_token["exp"] = datetime.utcnow() + TOKEN_EXPIRATION

    return encode_token(decoded_token)


def get_exp_time_of_token_itself(token: str):
    # decode the token
    decoded_token = decode_jwt_token(token)

    # get its expiration time
    exp_time = decoded_token["exp"]

    return exp_time


# Function to verify and decode a JWT token
def decode_jwt_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None


# def make_token(item: dict):
#     data = item.copy()
#     expire = datetime.utcnow() + TOKEN_EXPIRATION
#     data.update({"exp": expire})

#     # Generate an access token
#     access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

#     # Bind user ID to token
#     token_id = str(data.get("sub"))

#     #   Store the token ID in Redis with an expiration time
#     redis_client.setex(token_id, TOKEN_EXPIRATION.seconds, access_token)

#     return access_token


# def verify_token(token: str):
#     # Check if the token exists in Redis
#     for key in redis_client.keys(pattern="*"):
#         exact_token = redis_client.get(key).decode("utf-8")
#         if exact_token == token:
#             return jwt.decode(
#                 token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_sub": False}
#             ).get("sub")

#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail={"error": "Token expired or invalid"},
#     )
