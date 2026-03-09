from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None

    @classmethod
    def ok(cls, data: T = None, message: str | None = None) -> "ApiResponse[T]":
        return cls(success=True, data=data, message=message)

    @classmethod
    def fail(cls, message: str) -> "ApiResponse":
        return cls(success=False, message=message)


class PageResponse(BaseModel, Generic[T]):
    content: list[T]
    total_elements: int
    total_pages: int
    page: int
    size: int

    @classmethod
    def of(cls, content: list[T], total_elements: int, page: int, size: int) -> "PageResponse[T]":
        total_pages = (total_elements + size - 1) // size if size > 0 else 0
        return cls(
            content=content,
            total_elements=total_elements,
            total_pages=total_pages,
            page=page,
            size=size,
        )
