from app.board.repository.query_repository import BoardQueryRepository, PostQueryRepository
from app.board.schemas import (
    AuthorResponse,
    BoardResponse,
    FileInfoResponse,
    PostListResponse,
    PostResponse,
)
from app.common.exceptions import NotFoundException
from app.common.pagination import SortOrder


class BoardQueryService:
    def __init__(self):
        self.repo = BoardQueryRepository()

    async def get_board_list(self) -> list[BoardResponse]:
        rows = await self.repo.select_board_list()
        return [BoardResponse(**dict(row)) for row in rows]

    async def get_board_by_id(self, board_id: str) -> BoardResponse:
        row = await self.repo.select_board_by_id(board_id)
        if row is None:
            raise NotFoundException("게시판을 찾을 수 없습니다.")
        return BoardResponse(**dict(row))


class PostQueryService:
    def __init__(self):
        self.repo = PostQueryRepository()

    async def get_post_list(
        self,
        board_id: str,
        search: str | None,
        search_type: str | None,
        sort_order: SortOrder,
        limit: int,
        offset: int,
    ) -> list[PostListResponse]:
        rows = await self.repo.select_post_list(board_id, search, search_type, sort_order, limit, offset)
        return [PostListResponse(**dict(row)) for row in rows]

    async def get_post_count(
        self, board_id: str, search: str | None, search_type: str | None
    ) -> int:
        return await self.repo.select_post_count(board_id, search, search_type)

    async def get_post_detail(self, post_id: int) -> PostResponse:
        row = await self.repo.select_post_by_id(post_id)
        if row is None:
            raise NotFoundException("게시글을 찾을 수 없습니다.")

        file_rows = await self.repo.select_post_files(post_id)

        author = AuthorResponse(
            id=row["author_id"] or "",
            username=row["author_id"] or "",
            name=row["author_name"] or "",
            email=row["author_email"],
            role="USER",
        )

        files = [
            FileInfoResponse(
                id=f["id"],
                originalName=f["original_name"],
                storedName=f["stored_name"],
                size=f["size"] or 0,
                contentType=f["content_type"],
            )
            for f in file_rows
        ]

        return PostResponse(
            id=row["id"],
            boardId=row["board_id"],
            title=row["title"],
            content=row["content"],
            author=author,
            viewCount=row["view_count"] or 0,
            files=files,
            createdAt=row["created_date"],
            updatedAt=row["modified_date"],
        )

    async def get_recent_posts(self) -> list[PostListResponse]:
        rows = await self.repo.select_recent_posts()
        return [PostListResponse(**dict(row)) for row in rows]
