import httpx


class TestAdmin:
    async def test_admin_get_user_list(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/users", headers=admin_headers)
        assert resp.status_code == 200

    async def test_admin_get_user_by_id(self, client: httpx.AsyncClient, admin_headers: dict):
        # admin 사용자의 상세 조회
        resp = await client.get("/api/v1/admin/users/admin", headers=admin_headers)
        assert resp.status_code == 200

    async def test_admin_dashboard_stats(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/dashboard/stats", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_admin_recent_users(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/dashboard/recent-users", headers=admin_headers)
        assert resp.status_code == 200

    async def test_admin_board_list(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/boards", headers=admin_headers)
        assert resp.status_code == 200

    async def test_admin_forbidden_for_normal_user(self, client: httpx.AsyncClient, user_headers: dict):
        resp = await client.get("/api/v1/admin/users", headers=user_headers)
        assert resp.status_code == 403
