# fastapi-cqrs — Progress

## Phase 0: 프로젝트 스캐폴딩

- [x] FastAPI 앱 구조 (main.py, lifespan)
- [x] pydantic-settings 환경 설정
- [x] asyncpg 커넥션 풀
- [x] 예외 처리 (BusinessException, exception_handlers)
- [x] 공통 응답 (ApiResponse, PageResponse)
- [x] 요청 로깅 미들웨어
- [x] JWT + BCrypt 보안 모듈

## Phase 1: 인증 모듈

- [x] 로그인 (JWT 생성)
- [x] 회원가입 (BCrypt 해싱)
- [x] 토큰 갱신
- [x] 로그인 이력 추적

## Phase 2: 사용자 모듈

- [x] 프로필 조회
- [x] 프로필 수정
- [x] 비밀번호 변경

## Phase 3: 게시판/게시글 모듈

- [x] 게시판 목록/상세
- [x] 게시글 CRUD
- [x] 페이지네이션 + 검색
- [x] 최근 게시글
- [x] 조회수 증가

## Phase 4: 파일 모듈

- [x] 파일 업로드 (UUID, aiofiles)
- [x] 파일 다운로드

## Phase 5: 대시보드 모듈

- [x] 통계 집계
- [x] 차트 데이터 (generate_series)

## Phase 6: AI 채팅 모듈

- [x] SSE 스트리밍
- [x] Anthropic 프로바이더
- [x] OpenAI 프로바이더
- [x] Gemini 프로바이더

## Phase 7: 관리자 모듈

- [x] 관리자 대시보드
- [x] 사용자 관리 (목록/생성/수정/활성화 토글)
- [x] 게시판 관리

## Phase 8: 시스템 모듈

- [x] 역할 관리
- [x] 메뉴 관리 (계층 트리)
- [x] 메뉴-역할 매핑
- [x] 공통코드 관리
- [x] 직급-역할 매핑
- [x] 내 메뉴 API

## Phase 9: 통합 테스트

- [x] test_health (1개)
- [x] test_auth (7개)
- [x] test_board (9개)
- [x] test_user (4개)
- [x] test_file (3개)
- [x] test_admin (6개)
- [x] test_system (6개)
- [x] test_dashboard (2개)
- [x] test_ai (2개)
