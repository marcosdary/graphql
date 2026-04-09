from app.config import redis_client_async
from app.dto.user import UserListModel
from app.repositories import UserRepository

class UserCacheService:

    def __init__(self) -> None:
        self._user_repo = UserRepository()

    async def get_cached_data(self, key: str):
        return await redis_client_async.get(key)

    async def list_users(self, page: int, limit: int) -> UserListModel:
        key = f"users:{page}:{limit}"
        cached = await self.get_cached_data(key)

        if cached:
            return UserListModel.model_validate_json(cached)
        
        users = await self._user_repo.list_users(page, limit)
      
        await redis_client_async.set(key, users.model_dump_json(), 60 * 4)
        return users
        
