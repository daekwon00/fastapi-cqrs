import httpx


class TestSystem:
    async def test_get_role_list(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/roles", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_get_menu_list(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/menus", headers=admin_headers)
        assert resp.status_code == 200

    async def test_get_my_menus(self, client: httpx.AsyncClient, user_headers: dict):
        resp = await client.get("/api/v1/menus/my", headers=user_headers)
        assert resp.status_code == 200

    async def test_get_code_group_list(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/code-groups", headers=admin_headers)
        assert resp.status_code == 200

    async def test_get_menu_roles(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/menu-roles", headers=admin_headers)
        assert resp.status_code == 200

    async def test_get_position_roles(self, client: httpx.AsyncClient, admin_headers: dict):
        resp = await client.get("/api/v1/admin/position-roles", headers=admin_headers)
        assert resp.status_code == 200
