# Phase 1: 인증 모듈

## 상태: 완료

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | /api/v1/auth/login | 로그인 |
| POST | /api/v1/auth/register | 회원가입 |
| POST | /api/v1/auth/refresh | 토큰 갱신 |

## 작업 내용

- [x] auth/router.py — 3개 엔드포인트
- [x] command_service — login(), register()
- [x] query_service — get_login_history()
- [x] command_repository / query_repository
- [x] JWT 생성 (accessToken + refreshToken)
- [x] BCrypt 비밀번호 해싱
- [x] 로그인 이력 추적 (try/except FK 대응)
