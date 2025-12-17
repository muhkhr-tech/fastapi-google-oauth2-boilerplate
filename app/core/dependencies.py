from fastapi import Header

from app.core.redis import redis_client
from app.core.jwt_handler import verify_token
from app.core.exceptions import AuthError

async def get_redis():
    return redis_client

async def get_current_user(authorization: str = Header(...)):
    print(authorization,'autnih')
    try:
        token = authorization.split(" ")[1] # remove Bearer
        payload = await verify_token(token)
        return payload
    except Exception as e:
        raise AuthError(401, 'Invalid token!') from e
