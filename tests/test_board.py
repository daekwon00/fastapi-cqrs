import httpx
import pytest


class TestBoardRead:
    async def test_get_board_list(self, client: httpx.AsyncClient):
        resp = await client.get("/api/v1/boards")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)

    async def test_get_board_by_id(self, client: httpx.AsyncClient):
        # 먼저 목록에서 첫 번째 게시판 ID를 가져옴
        boards = (await client.get("/api/v1/boards")).json()["data"]
        if not boards:
            pytest.skip("게시판 데이터 없음")
        board_id = boards[0]["id"]

        resp = await client.get(f"/api/v1/boards/{board_id}")
        assert resp.status_code == 200
        assert resp.json()["data"]["id"] == board_id

    async def test_get_board_not_found(self, client: httpx.AsyncClient):
        resp = await client.get("/api/v1/boards/nonexistent-board-id")
        assert resp.status_code == 404


class TestPostCRUD:
    """게시글 CRUD 순서 보장: create → read → update → delete"""

    _created_post_id: int | None = None
    _board_id: str | None = None

    async def test_create_post(self, client: httpx.AsyncClient, user_headers: dict):
        boards = (await client.get("/api/v1/boards")).json()["data"]
        if not boards:
            pytest.skip("게시판 데이터 없음")
        TestPostCRUD._board_id = boards[0]["id"]

        resp = await client.post(
            "/api/v1/posts",
            json={
                "boardId": self._board_id,
                "title": "테스트 게시글",
                "content": "통합 테스트 본문입니다.",
            },
            headers=user_headers,
        )
        assert resp.status_code == 201
        TestPostCRUD._created_post_id = resp.json()["data"]["id"]

    async def test_get_post_detail(self, client: httpx.AsyncClient):
        if not self._created_post_id:
            pytest.skip("게시글 미생성")
        resp = await client.get(f"/api/v1/posts/{self._created_post_id}")
        assert resp.status_code == 200
        assert resp.json()["data"]["title"] == "테스트 게시글"

    async def test_get_post_list_pagination(self, client: httpx.AsyncClient):
        if not self._board_id:
            pytest.skip("게시판 ID 없음")
        resp = await client.get(f"/api/v1/boards/{self._board_id}/posts?page=1&size=5")
        assert resp.status_code == 200
        page_data = resp.json()["data"]
        assert "content" in page_data
        assert "total_elements" in page_data

    async def test_update_post(self, client: httpx.AsyncClient, user_headers: dict):
        if not self._created_post_id:
            pytest.skip("게시글 미생성")
        resp = await client.put(
            f"/api/v1/posts/{self._created_post_id}",
            json={"title": "수정된 제목", "content": "수정된 본문"},
            headers=user_headers,
        )
        assert resp.status_code == 200

    async def test_delete_post(self, client: httpx.AsyncClient, user_headers: dict):
        if not self._created_post_id:
            pytest.skip("게시글 미생성")
        resp = await client.delete(
            f"/api/v1/posts/{self._created_post_id}",
            headers=user_headers,
        )
        assert resp.status_code == 200

    async def test_get_recent_posts(self, client: httpx.AsyncClient):
        resp = await client.get("/api/v1/posts/recent")
        assert resp.status_code == 200
        assert resp.json()["success"] is True
