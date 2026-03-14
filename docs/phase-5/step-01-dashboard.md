# Phase 5: 대시보드 모듈

## 상태: 완료

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | /api/v1/dashboard/stats | 통계 |
| GET | /api/v1/dashboard/chart | 차트 데이터 |

## 작업 내용

- [x] dashboard/router.py — 2개 엔드포인트
- [x] query_service — get_stats(), get_chart_data()
- [x] query_repository — generate_series 활용
