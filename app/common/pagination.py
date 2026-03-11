from enum import Enum

from fastapi import Query


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class PagingParams:
    def __init__(
        self,
        page: int = Query(0, ge=0, description="페이지 번호 (0-based)"),
        size: int = Query(10, ge=1, le=100, description="페이지 크기"),
        sort_order: SortOrder = Query(SortOrder.DESC, alias="sortOrder", description="정렬 순서"),
    ):
        self.page = page
        self.size = size
        self.sort_order = sort_order

    @property
    def offset(self) -> int:
        return self.page * self.size

    @property
    def limit(self) -> int:
        return self.size
