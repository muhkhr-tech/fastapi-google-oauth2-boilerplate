from fastapi import APIRouter, Depends

from app.core.response import success_response
from app.core.dependencies import get_current_user

router = APIRouter(tags=["USERS"])

@router.get("/users/me")
async def login(current_user = Depends(get_current_user)):

    return success_response(
        data={
            **current_user
        },
    )