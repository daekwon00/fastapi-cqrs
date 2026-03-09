import asyncpg

from app.common.exceptions import NotFoundException
from app.file.repository.query_repository import FileQueryRepository


class FileQueryService:
    def __init__(self):
        self.repo = FileQueryRepository()

    async def get_file_by_id(self, file_id: str) -> asyncpg.Record:
        row = await self.repo.select_file_by_id(file_id)
        if row is None:
            raise NotFoundException("파일을 찾을 수 없습니다.")
        return row
