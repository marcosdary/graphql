import jwt

from app.constants import redisClient

class BaseService:

    def _encode(self, payload: dict, key: str) -> str:
        return jwt.encode(payload, key, "HS256")

    def _decode(self, token: str, key: str) -> dict:
        return jwt.decode(token, key, "HS256")

    def _store_with_expiration(self, key: str, value, expiration: int):
        redisClient.setex(key, expiration, value)

    def _get_or_none(self, key: str):
        return redisClient.get(key)

    def _delete(self, key: str):
        redisClient.delete(key)