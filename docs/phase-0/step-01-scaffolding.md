# Phase 0: 프로젝트 스캐폴딩

## 상태: 완료

## 작업 내용

- [x] FastAPI 앱 (main.py)
  - lifespan으로 DB 풀 생명주기 관리
  - CORS 미들웨어 (localhost:3000 허용)
  - 라우터 등록 (14개 도메인)
- [x] 환경 설정 (config.py)
  - pydantic-settings 기반
  - DB, JWT, AI API 키, 파일 업로드 경로
- [x] DB 커넥션 풀 (database.py)
  - asyncpg.create_pool()
  - search_path=internal 설정
- [x] 보안 모듈 (security/)
  - jwt.py — HS256, accessToken 1h / refreshToken 7d
  - password.py — BCrypt 해싱
  - dependencies.py — get_current_user, require_admin
- [x] 공통 모듈 (common/)
  - schemas.py — ApiResponse[T], PageResponse[T]
  - exceptions.py — BusinessException
  - exception_handlers.py — 전역 핸들러
  - pagination.py — PagingParams, SortOrder
  - middleware.py — RequestLoggingMiddleware
