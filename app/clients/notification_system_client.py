import asyncio

from requests import post

from app.config import settings

class NotificationSystemClient:
    def __init__(self):
        self._base_url = settings.URL_NOTIFICATION_SYSTEM
        self._api_key = settings.API_KEY

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
    
    async def execute_request(self, query: str, variables=None) -> dict:
        headers = self._headers()

        response = await asyncio.to_thread(
            post,
            url=self._base_url,
            headers=headers,
            json={
                "query": query,
                "variables": variables or {}
            },
        )

        data = response.json()

        return data