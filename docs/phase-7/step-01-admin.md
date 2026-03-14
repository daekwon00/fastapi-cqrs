# Phase 7: 관리자 모듈

## 상태: 완료

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | /api/v1/admin/dashboard/stats | 관리자 통계 |
| GET | /api/v1/admin/dashboard/recent-users | 최근 가입자 |
| GET | /api/v1/admin/users | 사용자 목록 |
| GET | /api/v1/admin/users/{id} | 사용자 상세 |
| POST | /api/v1/admin/users | 사용자 생성 |
| PUT | /api/v1/admin/users/{id} | 사용자 수정 |
| PATCH | /api/v1/admin/users/{id}/toggle-active | 활성화 토글 |
| GET | /api/v1/admin/boards | 게시판 목록 |
| POST | /api/v1/admin/boards | 게시판 생성 |
| PUT | /api/v1/admin/boards/{id} | 게시판 수정 |
| PATCH | /api/v1/admin/boards/{id}/toggle-active | 활성화 토글 |

## 작업 내용

- [x] admin/user — 사용자 관리 (CRUD + 페이지네이션 + 검색)
- [x] admin/board — 게시판 관리 (CRUD + 활성화)
- [x] admin/dashboard — 통계 + 최근 가입자
