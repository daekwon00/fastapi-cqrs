from fastapi import APIRouter, Depends, status

from app.common.schemas import ApiResponse
from app.security.dependencies import CurrentUser, get_current_user, require_admin
from app.system.role.schemas import CreateRoleRequest, RoleResponse, UpdateRoleRequest
from app.system.role.service.command_service import RoleCommandService
from app.system.role.service.query_service import RoleQueryService

router = APIRouter(prefix="/api/v1/admin/roles", tags=["System Role"], dependencies=[Depends(require_admin)])
query_service = RoleQueryService()
command_service = RoleCommandService()


@router.get("", response_model=ApiResponse[list[RoleResponse]])
async def get_role_list():
    return ApiResponse.ok(await query_service.get_role_list())


@router.post("", response_model=ApiResponse[RoleResponse], status_code=status.HTTP_201_CREATED)
async def create_role(request: CreateRoleRequest, user: CurrentUser = Depends(get_current_user)):
    await command_service.create_role(request.id, request.name, request.description, user.user_id)
    return ApiResponse.ok(await query_service.get_role_by_id(request.id))


@router.put("/{role_id}", response_model=ApiResponse[RoleResponse])
async def update_role(role_id: str, request: UpdateRoleRequest, user: CurrentUser = Depends(get_current_user)):
    await command_service.update_role(role_id, request.name, request.description, user.user_id)
    return ApiResponse.ok(await query_service.get_role_by_id(role_id))


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: str):
    await command_service.delete_role(role_id)
