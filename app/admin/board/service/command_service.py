from app.admin.board.repository.command_repository import AdminBoardCommandRepository


class AdminBoardCommandService:
    def __init__(self):
        self.repo = AdminBoardCommandRepository()

    async def create_board(self, board_id: str, name: str, description: str | None, created_by: str):
        await self.repo.insert_board(board_id, name, description, created_by)

    async def update_board(self, board_id: str, name: str, description: str | None, modified_by: str):
        await self.repo.update_board(board_id, name, description, modified_by)

    async def toggle_active(self, board_id: str):
        await self.repo.toggle_active(board_id)
