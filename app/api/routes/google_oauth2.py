from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from app.services.google_oauth2 import get_google_oauth2_service, GoogleOAuth2Service
from app.services.user_service import get_user_service, UserService
from app.core.response import success_response
router = APIRouter(tags=["Google OAuth2"])

@router.get("/google-oauth2/login")
async def google_oauth2_login(oauth_service = Depends(get_google_oauth2_service)):

    authorization_url = await oauth_service.generate_authorization_url()

    return RedirectResponse(authorization_url)

@router.get("/google-oauth2/callback", response_model=None)
async def google_oauth2_callback(
    request: Request,
    oauth_service: GoogleOAuth2Service = Depends(get_google_oauth2_service),
    user_service: UserService = Depends(get_user_service)
):
    
    authorization_url = str(request.url)
    state = request.query_params.get('state')

    oauth_data = await oauth_service.get_token(authorization_url, state)

    user = await user_service.login_with_google(
        email=oauth_data["email"],
        name=oauth_data["name"],
        refresh_token=oauth_data["refresh_token"]
    )

    print(user,'nihuser')
    
    return success_response(
        data={
            "email": user["email"],
            "name": user["name"],
        },
        message="Login with Google successful",
    )


@router.get("/google-oauth2/user")
async def google_oauth2_user(request: Request, user_service = Depends(get_user_service)):

    user = await user_service.get_user(request.query_params.get('email'))

    data = {
        "email": user
    }

    return success_response(
        data=data
    )
    
