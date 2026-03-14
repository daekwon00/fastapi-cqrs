# Phase 4: 파일 모듈

## 상태: 완료

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | /api/v1/files/upload | 파일 업로드 |
| GET | /api/v1/files/{id}/download | 파일 다운로드 |

## 작업 내용

- [x] file/router.py — 2개 엔드포인트
- [x] command_service — upload (UUID 네이밍, aiofiles)
- [x] query_service — download
- [x] command_repository / query_repository
