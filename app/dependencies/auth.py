from fastapi import Header

from app.core.security.jwt import verify_token
from app.core.exceptions.service import AuthError

async def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1] # remove Bearer
        payload = verify_token(token)
        return payload
    except Exception as e:
        raise AuthError('Invalid token!') from e