# Phase 8: 시스템 모듈

## 상태: 완료

## 엔드포인트 (18개)

- 역할: GET/POST/PUT/DELETE /api/v1/system/roles
- 메뉴: GET/POST/PUT/DELETE /api/v1/system/menus + GET /api/v1/menus/my
- 메뉴-역할: GET/PUT /api/v1/system/menu-roles
- 공통코드: GET groups + GET/POST/PUT/DELETE codes
- 직급-역할: GET/PUT /api/v1/system/position-roles

## 작업 내용

- [x] system/role — 역할 CRUD
- [x] system/menu — 메뉴 관리 (계층 트리, flat→tree 변환)
- [x] system/menu_role — 메뉴-역할 매핑 (벌크 할당)
- [x] system/code — 공통코드 (그룹 + 코드)
- [x] system/position_role — 직급-역할 매핑 (벌크 할당)
- [x] 내 메뉴 API (역할 기반)
