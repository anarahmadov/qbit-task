from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
import redis

# Create a connection to Redis
redis_client = redis.StrictRedis(host="redis-container", port=6379, db=0)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
TOKEN_EXPIRATION = timedelta(hours=1)


# util functions to save and retrieve token from Redis


# get the token from Redis
def retrieve_token_from_redis(token_id: str):
    return redis_client.get(token_id)


# save the token on Redis
def save_token_on_redis(
    token_id: str, token: str, expiration_time: timedelta() = TOKEN_EXPIRATION.seconds
):
    return redis_client.set(token_id, token, expiration_time)


# remove the token from Redis
def remove_token_from_redis(token_id: str):
    redis_client.delete(token_id)


# util functions


# Function to track user activity and update the token expiration time
def if_token_exists_then_update(token_id: str):
    # get the token from redis
    actual_token = retrieve_token_from_redis(token_id)

    if not actual_token:
        return False

    # Store that token in Redis, Redis ID with an expiration time
    save_token_on_redis(token_id, actual_token, TOKEN_EXPIRATION.seconds)

    return True


def revoke_if_inactive(token_id: str):
    if token_id:
        token = retrieve_token_from_redis(token_id)
        if not token:
            return False
