# Phase 9: 통합 테스트

## 상태: 완료 (40개 ALL PASSED, 1.83초)

## 테스트 구성

| 파일 | 테스트 수 | 대상 |
|------|----------|------|
| test_health.py | 1 | 헬스 체크 |
| test_auth.py | 7 | 인증 (등록/로그인/갱신/검증) |
| test_board.py | 9 | 게시판/게시글 CRUD + 페이지네이션 |
| test_user.py | 4 | 프로필, 비밀번호 변경 |
| test_file.py | 3 | 업로드, 다운로드, 인증 |
| test_admin.py | 6 | 관리자 엔드포인트, 권한 검증 |
| test_system.py | 6 | 역할, 메뉴, 코드, 매핑 |
| test_dashboard.py | 2 | 통계, 차트 |
| test_ai.py | 2 | SSE 인증, 프로바이더 검증 |

## 작업 내용

- [x] conftest.py — pytest fixture (client, 토큰, DB 풀)
- [x] httpx.AsyncClient + ASGITransport (uvicorn 불필요)
- [x] session-scoped event loop
- [x] 실제 PostgreSQL (모킹 없음)
- [x] 테스트 후 DB 정리 (teardown)

## 해결한 이슈

- passlib + bcrypt 5.x 비호환 → bcrypt 직접 사용
- login_history FK 제약 → try/except 처리
- event loop scope 불일치 → pytest-asyncio 설정
