import jwt

from app.config import redis_client_async

class BaseService:

    def _encode(self, payload: dict, key: str) -> str:
        return jwt.encode(payload, key, "HS256")

    def _decode(self, token: str, key: str) -> dict:
        return jwt.decode(token, key, algorithms=["HS256"])

    async def _store_with_expiration(self, key: str, value, expiration: int):
        await redis_client_async.set(key, value, expiration)

    async def _consume_or_none(self, key: str):
        return await redis_client_async.getdel(key)
    
    async def _fetch_or_none(self, key: str):
        return await redis_client_async.get(key)

    async def _delete(self, key: str) -> None:
        await redis_client_async.delete(key)