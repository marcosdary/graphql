from redis import Redis as RedisSync
from redis.asyncio import Redis 

from app.config.settings import settings

redis_client = RedisSync.from_url(
    url=settings.REDIS_URL, 
    decode_responses=True
)

redis_client_async = Redis.from_url(
    url=settings.REDIS_URL,
    decode_responses=True
)

