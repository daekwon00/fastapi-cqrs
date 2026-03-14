# Phase 2: 사용자 모듈

## 상태: 완료

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | /api/v1/users/me | 프로필 조회 |
| PUT | /api/v1/users/me | 프로필 수정 |
| PUT | /api/v1/users/me/password | 비밀번호 변경 |

## 작업 내용

- [x] user/router.py — 3개 엔드포인트
- [x] command_service — update_profile(), change_password()
- [x] query_service — get_user_info()
- [x] command_repository / query_repository
