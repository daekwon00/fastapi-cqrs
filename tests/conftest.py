import tempfile
import uuid

import httpx
import pytest

from app.database import create_pool, close_pool, get_pool
from app.main import app
from app.security.jwt import create_access_token


@pytest.fixture(scope="session")
async def client():
    """httpx AsyncClient + DB pool 수동 관리 (ASGITransport는 lifespan 미지원)"""
    await create_pool()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c
    await close_pool()


@pytest.fixture(scope="session")
def test_user_id():
    return uuid.uuid4().hex[:12]


@pytest.fixture(scope="session")
async def registered_user(client: httpx.AsyncClient, test_user_id: str):
    """테스트 사용자 등록 + teardown 시 DB 삭제"""
    username = f"testuser_{test_user_id}"
    password = "test1234"
    payload = {
        "username": username,
        "password": password,
        "name": "테스트사용자",
        "email": f"{username}@test.com",
    }
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201, f"등록 실패: {resp.text}"
    data = resp.json()["data"]

    yield {"username": username, "password": password, "user_id": data["id"], **data}

    # teardown: DB에서 사용자 삭제
    try:
        pool = get_pool()
        await pool.execute("DELETE FROM tb_user_role WHERE user_id = $1", data["id"])
        await pool.execute("DELETE FROM tb_user WHERE user_id = $1", data["id"])
    except Exception:
        pass  # pool이 이미 닫힌 경우 무시


@pytest.fixture(scope="session")
async def user_token(client: httpx.AsyncClient, registered_user: dict):
    """로그인 후 access_token 반환"""
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": registered_user["username"], "password": registered_user["password"]},
    )
    assert resp.status_code == 200
    return resp.json()["data"]["accessToken"]


@pytest.fixture(scope="session")
def user_headers(user_token: str):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture(scope="session")
def admin_token():
    """admin 사용자의 access_token 직접 생성"""
    return create_access_token("admin", ["ROLE_ADMIN"])


@pytest.fixture(scope="session")
def admin_headers(admin_token: str):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="session", autouse=True)
def override_upload_dir(tmp_path_factory):
    """FILE_UPLOAD_DIR을 임시 경로로 변경"""
    from app.config import settings

    original = settings.FILE_UPLOAD_DIR
    tmp_dir = tmp_path_factory.mktemp("uploads")
    settings.FILE_UPLOAD_DIR = str(tmp_dir)
    yield
    settings.FILE_UPLOAD_DIR = original
