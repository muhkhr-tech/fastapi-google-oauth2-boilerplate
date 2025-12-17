from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, update, insert
from fastapi import Depends
import datetime

from app.models.user import User
from app.core.exceptions import AppException
from app.core.database import get_db
from app.core.dependencies import get_redis

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_google_user(self, email: str, password: str, name: str, refresh_token: str | None):
        stmt = (
            insert(User)
            .values(
                email=email,
                name=name,
                password=password,
                refresh_token=refresh_token
            )
            .returning(
                User.email,
                User.name
            )
        )

        result = await self.db.execute(stmt)
        await self.db.commit()

        row = result.mappings().first()
        
        return dict(row) if row else None

    async def create(self, email: str, password: str, name: str, refresh_token: str | None = None):
        stmt = (
            insert(User)
            .values(
                email=email,
                password=password,
                name=name,
                refresh_token=refresh_token
            )
            .returning(
                User.email,
                User.name
            )
        )

        result = await self.db.execute(stmt)
        await self.db.commit()

        row = result.mappings().first()
        
        return dict(row) if row else None
    
    async def update_refresh_token(self, email, refresh_token):
        stmt = (
            update(User)
            .where(User.email == email)
            .values(refresh_token=refresh_token, updated_at=datetime.datetime.now(datetime.timezone.utc))
            .returning(
                User.email,
                User.name
            )
        )

        result = await self.db.execute(stmt)
        await self.db.commit()

        row = result.mappings().first()
        return dict(row) if row else None

    async def get_by_email(self, email):
        query = text("""
            SELECT email, name, password
            FROM public.users
            WHERE email=:email
        """)

        result = await self.db.execute(query, {"email": email})
        row = result.mappings().first()

        if not row:
            return None

        return dict(row) if row else None

def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)