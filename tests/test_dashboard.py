import httpx


class TestDashboard:
    async def test_get_dashboard_stats(self, client: httpx.AsyncClient, user_headers: dict):
        resp = await client.get("/api/v1/dashboard/stats", headers=user_headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_get_chart_data(self, client: httpx.AsyncClient):
        resp = await client.get("/api/v1/dashboard/chart?period=7d")
        assert resp.status_code == 200
        assert resp.json()["success"] is True
