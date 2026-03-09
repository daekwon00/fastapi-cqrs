import uuid

import httpx
import pytest

from app.database import get_pool
from app.security.jwt import create_access_token


class TestRegister:
    async def test_register_success(self, client: httpx.AsyncClient):
        username = f"reg_{uuid.uuid4().hex[:8]}"
        resp = await client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": "pass1234",
                "name": "신규사용자",
                "email": f"{username}@test.com",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["success"] is True
        assert data["data"]["username"] == username

        # cleanup
        pool = get_pool()
        user_id = data["data"]["id"]
        await pool.execute("DELETE FROM tb_user_role WHERE user_id = $1", user_id)
        await pool.execute("DELETE FROM tb_user WHERE user_id = $1", user_id)

    async def test_register_duplicate(self, client: httpx.AsyncClient, registered_user: dict):
        resp = await client.post(
            "/api/v1/auth/register",
            json={
                "username": registered_user["username"],
                "password": "pass1234",
                "name": "중복",
                "email": "dup@test.com",
            },
        )
        assert resp.status_code in (400, 409)


class TestLogin:
    async def test_login_success(self, client: httpx.AsyncClient, registered_user: dict):
        resp = await client.post(
            "/api/v1/auth/login",
            json={"username": registered_user["username"], "password": registered_user["password"]},
        )
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["username"] == registered_user["username"]

    async def test_login_wrong_password(self, client: httpx.AsyncClient, registered_user: dict):
        resp = await client.post(
            "/api/v1/auth/login",
            json={"username": registered_user["username"], "password": "wrongpass"},
        )
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/api/v1/auth/login",
            json={"username": "nouser_xyz_999", "password": "whatever"},
        )
        assert resp.status_code == 401


class TestRefresh:
    async def test_refresh_token(self, client: httpx.AsyncClient, registered_user: dict):
        # 먼저 로그인
        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"username": registered_user["username"], "password": registered_user["password"]},
        )
        refresh_token = login_resp.json()["data"]["refreshToken"]

        resp = await client.post(
            "/api/v1/auth/refresh",
            json={"refreshToken": refresh_token},
        )
        assert resp.status_code == 200
        assert "accessToken" in resp.json()["data"]

    async def test_refresh_invalid_token(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/api/v1/auth/refresh",
            json={"refreshToken": "invalid.token.value"},
        )
        assert resp.status_code == 401
