# Phase 3: 게시판/게시글 모듈

## 상태: 완료

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | /api/v1/boards | 게시판 목록 |
| GET | /api/v1/boards/{id} | 게시판 상세 |
| GET | /api/v1/boards/{id}/posts | 게시글 목록 |
| POST | /api/v1/posts | 게시글 생성 |
| GET | /api/v1/posts/{id} | 게시글 상세 |
| PUT | /api/v1/posts/{id} | 게시글 수정 |
| DELETE | /api/v1/posts/{id} | 게시글 삭제 |
| GET | /api/v1/posts/recent | 최근 게시글 |

## 작업 내용

- [x] board/router.py — 8개 엔드포인트
- [x] command_service — CRUD + 조회수 증가
- [x] query_service — 페이지네이션 + 검색 (제목/작성자/전체)
- [x] command_repository / query_repository
