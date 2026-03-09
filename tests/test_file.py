import httpx


class TestFile:
    _uploaded_file_id: str | None = None

    async def test_upload_file(self, client: httpx.AsyncClient, user_headers: dict):
        file_content = b"test file content"
        resp = await client.post(
            "/api/v1/files/upload",
            files={"files": ("test.txt", file_content, "text/plain")},
            headers=user_headers,
        )
        assert resp.status_code == 201
        data = resp.json()["data"]
        assert isinstance(data, list)
        assert len(data) > 0
        TestFile._uploaded_file_id = data[0]["id"]

    async def test_download_file(self, client: httpx.AsyncClient):
        if not self._uploaded_file_id:
            import pytest
            pytest.skip("파일 미업로드")
        resp = await client.get(f"/api/v1/files/{self._uploaded_file_id}/download")
        assert resp.status_code == 200

    async def test_upload_unauthorized(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/api/v1/files/upload",
            files={"files": ("test.txt", b"data", "text/plain")},
        )
        assert resp.status_code in (401, 403)
