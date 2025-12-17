from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from fastapi import Depends

from app.core.exceptions.service import GoogleOAuthError
from app.core.config import settings
from app.dependencies.redis import get_redis

class GoogleOAuth2Service:
    def __init__(self, redis):
        self.redis = redis
        self.credentials = None
        try:
            self.flow = Flow.from_client_secrets_file(
                settings.GOOGLE_CLIENT_SECRET_PATH,
                scopes=settings.GOOGLE_SCOPES,
                redirect_uri=settings.GOOGLE_REDIRECT_URI
            )
        except FileNotFoundError:
            raise GoogleOAuthError('Client Secret path not found!')
        except Exception as e:
            raise GoogleOAuthError('Failed to initiate Google OAuth2!') from e

    async def generate_authorization_url(self):
        try:
            authorization_url, state = self.flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                # prompt='consent'
            )

            await self.redis.setex(
                f"oauth:state:{state}",
                300,
                "valid"
            )

            return authorization_url
        except Exception as e:
            raise GoogleOAuthError('Failed to generate authorization URL!') from e
        
    async def get_token(self, authorization_url, state):
        exists = await self.redis.get(f"oauth:state:{state}")

        if not exists:
            raise GoogleOAuthError('Invalid or expired OAuth state')
        
        try:
            self.flow.fetch_token(authorization_response=authorization_url)
            self.credentials = self.flow.credentials

            user_info = await self.get_user(self.credentials)
            email = user_info.get("email")
            name = user_info.get("name")

            if not email:
                raise GoogleOAuthError("Email not found from Google")
            
            await self.redis.setex(
                f"oauth:google:access_token:{email}",
                3600,
                self.credentials.token
            )

            await self.redis.delete(f"oauth:state:{state}")

            return {
                "email": email,
                "name": name,
                "access_token": self.credentials.token,
                "refresh_token": self.credentials.refresh_token 
            }
        except Exception as e:
            raise GoogleOAuthError('Failed to fetch token!') from e
        

    async def get_user(self, credentials):
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            return user_info
        except Exception as e:
            raise GoogleOAuthError('Failed to get user!')
        

def get_google_oauth2_service(redis = Depends(get_redis)):
    return GoogleOAuth2Service(redis)