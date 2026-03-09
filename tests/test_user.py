import httpx


class TestUser:
    async def test_get_my_profile(self, client: httpx.AsyncClient, user_headers: dict):
        resp = await client.get("/api/v1/users/me", headers=user_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "username" in data
        assert "email" in data

    async def test_update_my_profile(self, client: httpx.AsyncClient, user_headers: dict, registered_user: dict):
        resp = await client.put(
            "/api/v1/users/me",
            json={
                "name": "수정된이름",
                "email": registered_user["email"],
            },
            headers=user_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["data"]["name"] == "수정된이름"

    async def test_change_password(self, client: httpx.AsyncClient, user_headers: dict, registered_user: dict):
        resp = await client.put(
            "/api/v1/users/me/password",
            json={
                "currentPassword": registered_user["password"],
                "newPassword": "newpass1234",
            },
            headers=user_headers,
        )
        assert resp.status_code == 200

        # 원래 비밀번호로 복원
        await client.put(
            "/api/v1/users/me/password",
            json={
                "currentPassword": "newpass1234",
                "newPassword": registered_user["password"],
            },
            headers=user_headers,
        )

    async def test_get_profile_unauthorized(self, client: httpx.AsyncClient):
        resp = await client.get("/api/v1/users/me")
        assert resp.status_code in (401, 403)
