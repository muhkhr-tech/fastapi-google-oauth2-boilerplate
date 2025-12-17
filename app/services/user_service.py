from fastapi import Depends
from pwdlib import PasswordHash

from app.repositories.user_repo import get_user_repository, UserRepository
from app.core.exceptions.service import AuthError
from app.core.security.jwt import create_access_token
from app.utils.generate_random import secure_random_string

password_hash = PasswordHash.recommended()

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login_with_google(self, email, name, refresh_token):
        existing_user = await self.user_repo.get_by_email(email)

        if existing_user:
            if refresh_token:
                updated_user = await self.user_repo.update_refresh_token(email, refresh_token=refresh_token)
                return updated_user
            return existing_user
        
        hashed_password = await self.get_password_hash(secure_random_string())
        
        created_user = await self.user_repo.create_google_user(
            email=email,
            name=name,
            password=hashed_password,
            refresh_token=refresh_token
        )

        return created_user
    
    async def login(self, email, password):
        user = await self.user_repo.get_by_email(email)

        if not user:
            raise AuthError(400, 'Invalid email or password!')
        
        if not await self.verify_password(password, user.get('password')):
            raise AuthError(400, 'Invalid email or password!')
        
        access_token = create_access_token({"email": user.get('email'), "name": user.get('name')})

        return access_token
    
    async def get_password_hash(self, password):
        return password_hash.hash(password)
    
    async def verify_password(self, password, hashed_password):
        return password_hash.verify(password, hashed_password)
    
    async def register(self, email, password, name):
        existing_user = await self.user_repo.get_by_email(email)

        if existing_user:
            raise AuthError(401, f"User with email {email} already registered!")
        
        hashed_password = await self.get_password_hash(password)

        registered_user = await self.user_repo.create(email, hashed_password, name)

        return registered_user
    
    async def get_user(self, email):
        return await self.user_repo.get_user(email)
    
def get_user_service(user_repo = Depends(get_user_repository)):
    return UserService(user_repo)