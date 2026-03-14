# FastAPI CQRS Project

## 프로젝트 개요
- Spring Boot 기반 `~/workspace/ydk-lab/spring-cqrs` 프로젝트를 FastAPI로 재구현
- 동일한 PostgreSQL DB를 사용하며, 기존 테이블 구조 유지
- CQRS 패턴(Command/Query 분리) 적용

## 참조 프로젝트
- **Spring Boot 원본**: `~/workspace/ydk-lab/spring-cqrs`
- **소스 경로**: `src/main/java/kr/or/study/springcqrs/`
- **MyBatis SQL**: `src/main/resources/mapper/` (테이블 구조, 쿼리 참조용)
- **설정**: `src/main/resources/application.yaml`

## 기술 스택
- Python 3.12+
- FastAPI + Uvicorn
- PostgreSQL + asyncpg
- Pydantic v2 (스키마 검증)
- python-jose 또는 PyJWT (JWT 인증)
- passlib[bcrypt] (비밀번호 해싱)
- httpx (AI API 비동기 호출)
- sse-starlette (SSE 스트리밍)
- python-multipart (파일 업로드)
- pydantic-settings (환경 설정)

## 아키텍처 규칙
- CQRS 패턴 유지: command_service / query_service 분리
- 도메인별 모듈 구조: router, service, schemas, repository
- Repository 계층에서 asyncpg로 SQL 직접 실행 (ORM 미사용)
- JWT 기반 인증, 역할 기반 인가
- 공통 응답: ApiResponse, PageResponse 래퍼 사용

## 도메인 모듈 (구현 순서)
1. common (공통 응답, 예외, 보안)
2. auth (로그인, 회원가입, 토큰 갱신)
3. board (게시판, 게시글 CRUD, 페이지네이션)
4. file (파일 업로드/다운로드)
5. user (프로필, 비밀번호 변경)
6. dashboard (통계)
7. ai (AI 채팅 SSE - Anthropic, OpenAI, Gemini)
8. admin (사용자/게시판 관리)
9. system (역할, 메뉴, 공통코드, 직급-역할)

## 개발 규칙
- 커밋 메시지는 한글로 작성
- spring-cqrs의 MyBatis XML을 참조하여 동일한 SQL 쿼리 사용
- 기존 DB 테이블 스키마 변경 없이 호환
- 환경 변수는 .env 파일로 관리

## SDD (Spec-Driven Development)

- `prd.md` — 프로젝트 요구사항 정의
- `docs/progress.md` — Phase/Step별 진행 체크리스트
- `docs/phase-N/step-NN-*.md` — 단계별 작업 명세
- 새 작업 시작 전 progress.md 확인, 완료 시 체크 표시 업데이트
