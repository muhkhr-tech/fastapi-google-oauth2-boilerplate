from fastapi import APIRouter

from app.api.routes import google_oauth2, auth, user

api_router = APIRouter()
api_router.include_router(google_oauth2.router)
api_router.include_router(auth.router)
api_router.include_router(user.router)