from app.board.repository.command_repository import PostCommandRepository
from app.board.schemas import PostResponse
from app.board.service.query_service import PostQueryService


class PostCommandService:
    def __init__(self):
        self.command_repo = PostCommandRepository()
        self.query_service = PostQueryService()

    async def create_post(
        self, board_id: str, title: str, content: str | None, created_by: str, file_ids: list[str] | None
    ) -> PostResponse:
        post_id = await self.command_repo.insert_post(board_id, title, content, created_by)

        if file_ids:
            for file_id in file_ids:
                await self.command_repo.insert_post_file(post_id, file_id)

        return await self.query_service.get_post_detail(post_id)

    async def update_post(
        self, post_id: int, title: str, content: str | None, modified_by: str, file_ids: list[str] | None
    ) -> PostResponse:
        await self.command_repo.update_post(post_id, title, content, modified_by)

        await self.command_repo.delete_post_files(post_id)
        if file_ids:
            for file_id in file_ids:
                await self.command_repo.insert_post_file(post_id, file_id)

        return await self.query_service.get_post_detail(post_id)

    async def delete_post(self, post_id: int):
        await self.command_repo.delete_post_files(post_id)
        await self.command_repo.delete_post(post_id)

    async def increase_view_count(self, post_id: int):
        await self.command_repo.update_view_count(post_id)
