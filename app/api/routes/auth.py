from fastapi import APIRouter, Depends, Body

from app.services.user_service import get_user_service, UserService
from app.api.responses import success_response
from app.schemas.auth_schema import LoginSchema, RegisterSchema

router = APIRouter(tags=["AUTH"])

@router.post("/auth/login")
async def login(body: LoginSchema = Body(...), user_service: UserService = Depends(get_user_service)):

    auth_login = await user_service.login(body.email, body.password)

    data = {
        "access_token": auth_login
    }

    return success_response(
        data=data,
        message='Login successfull!'
    )

@router.post("/auth/sign-up")
async def signin(body: RegisterSchema = Body(...), user_service: UserService = Depends(get_user_service)):

    await user_service.register(body.email, body.password, body.name)

    return success_response()

    
