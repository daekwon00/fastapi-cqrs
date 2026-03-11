# FastAPI CQRS

Spring Boot 기반 `spring-cqrs` 프로젝트를 FastAPI로 재구현한 백엔드 API 서버.
동일한 PostgreSQL DB(intranet/internal 스키마)를 공유하며, 기존 테이블 구조와 SQL 쿼리를 그대로 유지한다.

## 기술 스택

| 구분 | 기술 |
|------|------|
| Framework | FastAPI + Uvicorn |
| Language | Python 3.12+ |
| Database | PostgreSQL 17 + asyncpg (ORM 미사용, raw SQL) |
| 인증 | JWT (HS256) + BCrypt |
| 스키마 검증 | Pydantic v2 |
| AI 채팅 | httpx + sse-starlette (Anthropic/OpenAI/Gemini) |
| 패키지 매니저 | uv |

## 아키텍처

CQRS 패턴을 적용하여 Command(쓰기)와 Query(읽기)를 분리한다.

```
Router → CommandService → CommandRepository (INSERT/UPDATE/DELETE)
Router → QueryService   → QueryRepository   (SELECT)
```

## 프로젝트 구조

```
fastapi-cqrs/
├── app/
│   ├── main.py              # FastAPI 앱, lifespan, 미들웨어
│   ├── config.py             # pydantic-settings 환경설정
│   ├── database.py           # asyncpg 커넥션 풀
│   ├── common/               # 공통 응답, 예외, 페이지네이션
│   ├── security/             # JWT, 패스워드, 인증 Depends
│   ├── auth/                 # 로그인, 회원가입, 토큰갱신
│   ├── board/                # 게시판, 게시글 CRUD
│   ├── file/                 # 파일 업로드/다운로드
│   ├── user/                 # 프로필, 비밀번호 변경
│   ├── dashboard/            # 통계, 차트
│   ├── ai/                   # AI 채팅 SSE
│   ├── admin/                # 관리자 기능
│   └── system/               # 역할, 메뉴, 공통코드
├── tests/
├── pyproject.toml
├── Dockerfile
├── docker-compose.yaml
└── .env.example
```

각 도메인 모듈 내부:

```
{module}/
├── router.py
├── schemas.py
├── service/
│   ├── command_service.py
│   └── query_service.py
└── repository/
    ├── command_repository.py
    └── query_repository.py
```

## 실행 방법

### 사전 준비

- Python 3.12+
- PostgreSQL 17 (localhost:5432, intranet DB)
- uv 패키지 매니저

### 로컬 실행

```bash
# 의존성 설치
uv sync

# 환경변수 설정
cp .env.example .env
# .env 파일 편집

# 서버 실행
uv run uvicorn app.main:app --reload --port 8081
```

### Docker 실행

```bash
docker compose up -d
```

### 테스트 실행

```bash
# 전체 테스트
uv run pytest -v

# 특정 모듈만
uv run pytest tests/test_auth.py -v
```

> PostgreSQL 실행 필요 (localhost:5432, intranet DB, seed 데이터 포함)

### API 문서

서버 실행 후 접속:
- Swagger UI: http://localhost:8081/docs
- ReDoc: http://localhost:8081/redoc

## 환경변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| DB_HOST | DB 호스트 | localhost |
| DB_PORT | DB 포트 | 5432 |
| DB_USER | DB 사용자 | admin |
| DB_PASSWORD | DB 비밀번호 | - |
| DB_NAME | DB 이름 | intranet |
| DB_SCHEMA | DB 스키마 | internal |
| JWT_SECRET | JWT 서명 키 | - |
| APP_PORT | 서버 포트 | 8081 |
| FILE_UPLOAD_DIR | 파일 업로드 경로 | ./uploads |

## 참조

- 원본 프로젝트: [spring-cqrs](../spring-cqrs/) (Spring Boot 4 + Java 25 + MyBatis)
- 통합 테스트: 40개 (10개 도메인 모듈 커버)
