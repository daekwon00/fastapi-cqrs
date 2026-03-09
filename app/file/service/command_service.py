import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.config import settings
from app.file.repository.command_repository import FileCommandRepository
from app.file.schemas import FileResponse


class FileCommandService:
    def __init__(self):
        self.command_repo = FileCommandRepository()

    async def upload_files(self, files: list[UploadFile], user_id: str) -> list[FileResponse]:
        upload_path = Path(settings.FILE_UPLOAD_DIR).resolve()
        upload_path.mkdir(parents=True, exist_ok=True)

        responses: list[FileResponse] = []

        for file in files:
            file_id = str(uuid.uuid4())
            original_filename = file.filename or "unknown"
            extension = ""
            if "." in original_filename:
                extension = original_filename[original_filename.rfind("."):]
            stored_filename = file_id + extension
            file_path = upload_path / stored_filename

            content = await file.read()
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(content)

            file_size = len(content)
            content_type = file.content_type

            await self.command_repo.insert_file(
                file_id, original_filename, stored_filename,
                str(file_path), file_size, content_type, user_id,
            )

            responses.append(FileResponse(
                id=file_id,
                originalName=original_filename,
                storedName=stored_filename,
                size=file_size,
                contentType=content_type,
            ))

        return responses
