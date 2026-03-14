# fastapi-cqrs — PRD (Product Requirements Document)

## 프로젝트 개요

spring-cqrs 백엔드를 FastAPI(Python)로 재구현한 프로젝트.
동일한 PostgreSQL DB와 API 스펙을 유지하며, CQRS 패턴을 Python 방식으로 적용.

## 기술 스택

- FastAPI + Uvicorn (ASGI)
- Python 3.12+
- PostgreSQL + asyncpg (raw SQL, ORM 미사용)
- Pydantic v2 (스키마 검증, camelCase alias)
- python-jose (JWT) + bcrypt (비밀번호)
- httpx (AI API 비동기 호출)
- sse-starlette (SSE 스트리밍)
- aiofiles (비동기 파일 I/O)
- pydantic-settings (환경 설정)

## Phase 구성

### Phase 0: 프로젝트 스캐폴딩

- FastAPI 앱 구조, lifespan, 미들웨어
- pydantic-settings 기반 환경 설정
- asyncpg 커넥션 풀 관리
- 예외 처리 (BusinessException 등)
- 공통 응답 (ApiResponse, PageResponse)
- 요청 로깅 미들웨어

### Phase 1: 인증 모듈

- 로그인 (JWT 생성 + refresh token)
- 회원가입 (BCrypt 해싱)
- 토큰 갱신
- 로그인 이력 추적

### Phase 2: 사용자 모듈

- 프로필 조회/수정
- 비밀번호 변경

### Phase 3: 게시판/게시글 모듈

- 게시판 목록/상세
- 게시글 CRUD + 페이지네이션 + 검색
- 최근 게시글, 조회수 증가

### Phase 4: 파일 모듈

- 파일 업로드 (UUID 네이밍, aiofiles)
- 파일 다운로드

### Phase 5: 대시보드 모듈

- 통계 집계
- 차트 데이터 (generate_series)

### Phase 6: AI 채팅 모듈

- SSE 스트리밍
- 3개 프로바이더 (Anthropic / OpenAI / Gemini)
- 비동기 httpx 호출

### Phase 7: 관리자 모듈

- 관리자 대시보드 (통계 + 최근 가입자)
- 사용자 관리 (목록/생성/수정/활성화 토글)
- 게시판 관리

### Phase 8: 시스템 모듈

- 역할 관리 (CRUD)
- 메뉴 관리 (계층 트리)
- 메뉴-역할 매핑
- 공통코드 관리
- 직급-역할 매핑
- 내 메뉴 API

### Phase 9: 통합 테스트

- pytest + httpx.AsyncClient (40개 테스트)
- 실제 PostgreSQL 사용 (모킹 없음)
- fixture 기반 테스트 아키텍처
