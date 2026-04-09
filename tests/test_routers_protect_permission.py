import unittest
from unittest.mock import patch

from app.exceptions import ProtectedRouteError
from app.graphql.permissions.routers_protects_permission import check_session_permission


class _SessionServiceFake:
    def __init__(self, payload: dict):
        self._payload = payload

    async def verify_session(self, session_id: str) -> dict:
        return self._payload


class TestRoutersProtectPermission(unittest.IsolatedAsyncioTestCase):
    async def test_user_role_is_blocked(self):
        payload = {"userId": "u1", "role": "USER"}
        with patch(
            "app.graphql.permissions.routers_protects_permission.token.SessionService",
            return_value=_SessionServiceFake(payload),
        ):
            with self.assertRaises(ProtectedRouteError):
                await check_session_permission("session-1", "listUsers")

    async def test_admin_allowed_route_passes(self):
        payload = {"userId": "a1", "role": "ADMIN"}
        with patch(
            "app.graphql.permissions.routers_protects_permission.token.SessionService",
            return_value=_SessionServiceFake(payload),
        ):
            response = await check_session_permission("session-1", "listUsers")
            self.assertEqual(response, payload)

    async def test_admin_forbidden_route_fails(self):
        payload = {"userId": "a1", "role": "ADMIN"}
        with patch(
            "app.graphql.permissions.routers_protects_permission.token.SessionService",
            return_value=_SessionServiceFake(payload),
        ):
            with self.assertRaises(ProtectedRouteError):
                await check_session_permission("session-1", "createAdmin")

    async def test_super_admin_allowed_route_passes(self):
        payload = {"userId": "s1", "role": "SUPER_ADMIN"}
        with patch(
            "app.graphql.permissions.routers_protects_permission.token.SessionService",
            return_value=_SessionServiceFake(payload),
        ):
            response = await check_session_permission("session-1", "createAdmin")
            self.assertEqual(response, payload)

    async def test_super_admin_forbidden_route_fails(self):
        payload = {"userId": "s1", "role": "SUPER_ADMIN"}
        with patch(
            "app.graphql.permissions.routers_protects_permission.token.SessionService",
            return_value=_SessionServiceFake(payload),
        ):
            with self.assertRaises(ProtectedRouteError):
                await check_session_permission("session-1", "deleteApiKey")


if __name__ == "__main__":
    unittest.main()
