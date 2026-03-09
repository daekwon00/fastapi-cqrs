from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Depends, UploadFile, status
from starlette.responses import FileResponse as StarletteFileResponse

from app.common.schemas import ApiResponse
from app.file.schemas import FileResponse
from app.file.service.command_service import FileCommandService
from app.file.service.query_service import FileQueryService
from app.security.dependencies import CurrentUser, get_current_user

router = APIRouter(prefix="/api/v1/files", tags=["File"])
command_service = FileCommandService()
query_service = FileQueryService()


@router.post("/upload", response_model=ApiResponse[list[FileResponse]], status_code=status.HTTP_201_CREATED)
async def upload_files(
    files: list[UploadFile],
    current_user: CurrentUser = Depends(get_current_user),
):
    result = await command_service.upload_files(files, current_user.user_id)
    return ApiResponse.ok(result)


@router.get("/{file_id}/download")
async def download_file(file_id: str):
    file_info = await query_service.get_file_by_id(file_id)

    file_path = file_info["file_path"]
    original_name = file_info["original_name"]
    content_type = file_info["content_type"] or "application/octet-stream"

    encoded_filename = quote(original_name)

    return StarletteFileResponse(
        path=file_path,
        media_type=content_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        },
    )
