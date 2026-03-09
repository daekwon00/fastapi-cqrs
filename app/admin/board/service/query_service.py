from app.admin.board.repository.query_repository import AdminBoardQueryRepository
from app.admin.board.schemas import AdminBoardResponse
from app.common.exceptions import NotFoundException


class AdminBoardQueryService:
    def __init__(self):
        self.repo = AdminBoardQueryRepository()

    async def get_board_list(self) -> list[AdminBoardResponse]:
        rows = await self.repo.select_board_list()
        return [AdminBoardResponse(**dict(row)) for row in rows]

    async def get_board_by_id(self, board_id: str) -> AdminBoardResponse:
        row = await self.repo.select_board_by_id(board_id)
        if row is None:
            raise NotFoundException("게시판을 찾을 수 없습니다.")
        return AdminBoardResponse(**dict(row))
