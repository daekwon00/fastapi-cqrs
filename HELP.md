# 개발환경 구축 가이드

> macOS (Apple Silicon) / Homebrew 기준

---

## 1. 사전 요구사항

| 항목 | 버전 | 설치 방법 |
|------|------|-----------|
| Python | 3.12 ~ 3.13 | `uv python install 3.13` |
| PostgreSQL | 17+ | `brew install postgresql@17` |
| uv | 0.6+ | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Docker | 29+ | Docker Desktop |
| Git | 2.x | Xcode CLT 포함 |

> **주의**: Python 3.14는 asyncpg 등 핵심 패키지 호환성이 보장되지 않으므로 3.12 또는 3.13을 사용한다.

---

## 2. Python 환경 설정

```bash
cd ~/workspace/ydk-lab/fastapi-cqrs

# Python 3.13 설치
uv python install 3.13

# 가상환경 생성
uv venv --python 3.13

# 가상환경 활성화
source .venv/bin/activate

# 버전 확인
python --version  # Python 3.13.x
```

---

## 3. 패키지 설치

### 런타임 패키지

| 패키지 | 용도 |
|--------|------|
| fastapi | 웹 프레임워크 |
| uvicorn[standard] | ASGI 서버 |
| asyncpg | PostgreSQL 비동기 드라이버 (raw SQL) |
| pydantic[email] | 스키마 검증 (v2) |
| pydantic-settings | 환경설정 (.env 로딩) |
| python-jose[cryptography] | JWT 토큰 생성/검증 |
| passlib[bcrypt] | 비밀번호 해싱 |
| python-multipart | 파일 업로드 (UploadFile) |
| httpx | 비동기 HTTP 클라이언트 (AI API 호출) |
| sse-starlette | SSE 스트리밍 (AI 채팅) |
| aiofiles | 비동기 파일 IO |

### 개발 도구

| 패키지 | 용도 |
|--------|------|
| pytest | 테스트 프레임워크 |
| pytest-asyncio | 비동기 테스트 |
| ruff | 린터 + 포매터 |

### 설치 명령

> zsh에서 대괄호(`[]`)는 glob 패턴으로 해석되므로 반드시 따옴표로 감싼다.

```bash
source .venv/bin/activate

# 런타임
uv pip install fastapi 'uvicorn[standard]' asyncpg pydantic-settings \
  'python-jose[cryptography]' 'passlib[bcrypt]' python-multipart \
  httpx sse-starlette aiofiles

# 개발 도구
uv pip install pytest pytest-asyncio ruff
```

---

## 4. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일 편집:

```env
# Database (개별 파라미터 — 비밀번호 특수문자 파싱 이슈 방지)
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=your_password_here
DB_NAME=intranet
DB_SCHEMA=internal

# JWT
JWT_SECRET=spring-cqrs-local-dev-secret-key-must-be-at-least-256-bits-long-for-hs256
JWT_ACCESS_EXPIRATION=3600000
JWT_REFRESH_EXPIRATION=604800000

# File Upload
FILE_UPLOAD_DIR=./uploads

# Server
APP_HOST=0.0.0.0
APP_PORT=8081

# AI API Keys (필요 시 설정)
AI_DEFAULT_PROVIDER=anthropic
AI_ANTHROPIC_API_KEY=
AI_OPENAI_API_KEY=
AI_GEMINI_API_KEY=
```

> `APP_PORT=8081` — Spring Boot와 동일 포트로 대체 실행. 동시 실행 시 포트 충돌에 주의.

---

## 5. DB 접속 확인

```bash
# PostgreSQL 서버 상태
pg_isready

# 테이블 확인
psql -U admin -d intranet -c "SET search_path TO internal; SELECT count(*) FROM tb_user;"

# asyncpg 접속 테스트
python -c '
import asyncio, asyncpg

async def test():
    conn = await asyncpg.connect(
        host="localhost", port=5432,
        user="admin", password="your_password",
        database="intranet",
        server_settings={"search_path": "internal"}
    )
    result = await conn.fetchval("SELECT count(*) FROM tb_user")
    print(f"tb_user 레코드 수: {result}")
    await conn.close()

asyncio.run(test())
'
```

---

## 6. 서버 실행

```bash
# 개발 모드 (자동 리로드)
uv run uvicorn app.main:app --reload --port 8081

# API 문서 확인
# Swagger UI: http://localhost:8081/docs
# ReDoc:      http://localhost:8081/redoc
```

---

## 7. IDE 설정 (Cursor)

| 확장 | 필수 | 용도 |
|------|------|------|
| Python (ms-python) | 필수 | Python 지원 + 디버거 |
| Ruff | 권장 | 린터/포매터 |

> Pylance는 Cursor 마켓플레이스에서 미제공. Cursor 내장 AI 자동완성으로 대체.

---

## 8. 트러블슈팅

### zsh 특수문자

| 문자 | 문제 | 해결 |
|------|------|------|
| `[]` | glob 패턴 해석 | 따옴표: `'uvicorn[standard]'` |
| `!` | 히스토리 확장 | 작은따옴표로 감싸기 |
| `!@` (URL) | 파싱 오류 | 개별 파라미터 방식 사용 |

### DB 비밀번호 특수문자

URL 형식(`postgresql://admin:your_password@localhost/intranet`)은 파싱 실패.
개별 파라미터 방식을 사용한다:

```python
conn = await asyncpg.connect(
    host="localhost", port=5432,
    user="admin", password="your_password",
    database="intranet",
    server_settings={"search_path": "internal"}
)
```

### asyncpg 빌드 실패

```bash
xcode-select --install
```

### PostgreSQL 접속 실패

```bash
pg_isready
brew services restart postgresql@17
```

### Python 3.14 호환성 문제

```bash
uv venv --python 3.13 --force
source .venv/bin/activate
uv pip install -r requirements.txt
```
