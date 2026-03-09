from fastapi import APIRouter, Depends, status

from app.common.schemas import ApiResponse
from app.security.dependencies import CurrentUser, get_current_user, require_admin
from app.system.code.schemas import CodeGroupResponse, CodeResponse, CreateCodeRequest, UpdateCodeRequest
from app.system.code.service.command_service import CodeCommandService
from app.system.code.service.query_service import CodeQueryService

router = APIRouter(tags=["System Code"])
query_service = CodeQueryService()
command_service = CodeCommandService()


@router.get("/api/v1/admin/code-groups", response_model=ApiResponse[list[CodeGroupResponse]],
            dependencies=[Depends(require_admin)])
async def get_code_group_list():
    return ApiResponse.ok(await query_service.get_code_group_list())


@router.get("/api/v1/admin/codes", response_model=ApiResponse[list[CodeResponse]],
            dependencies=[Depends(require_admin)])
async def get_code_list(group_code: str | None = None):
    return ApiResponse.ok(await query_service.get_code_list(group_code))


@router.post("/api/v1/admin/codes", response_model=ApiResponse[CodeResponse],
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_code(request: CreateCodeRequest, user: CurrentUser = Depends(get_current_user)):
    code_id = f"{request.group_code}_{request.code}"
    await command_service.create_code(
        code_id, request.group_code, request.name, request.value,
        request.sort_order, request.description, user.user_id,
    )
    return ApiResponse.ok(await query_service.get_code_by_id(code_id))


@router.put("/api/v1/admin/codes/{code_id}", response_model=ApiResponse[CodeResponse],
            dependencies=[Depends(require_admin)])
async def update_code(code_id: str, request: UpdateCodeRequest, user: CurrentUser = Depends(get_current_user)):
    await command_service.update_code(
        code_id, request.group_code, request.name, request.value,
        request.sort_order, request.description, user.user_id,
    )
    return ApiResponse.ok(await query_service.get_code_by_id(code_id))


@router.delete("/api/v1/admin/codes/{code_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_admin)])
async def delete_code(code_id: str):
    await command_service.delete_code(code_id)
