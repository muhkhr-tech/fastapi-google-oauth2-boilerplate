from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis.from_url(
    settings.REDIS_URI,
    decode_responses=True
)