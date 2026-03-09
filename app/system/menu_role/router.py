from fastapi import APIRouter, Depends

from app.common.schemas import ApiResponse
from app.security.dependencies import CurrentUser, get_current_user, require_admin
from app.system.menu_role.schemas import MenuRoleResponse, UpdateMenuRoleRequest
from app.system.menu_role.service.command_service import MenuRoleCommandService
from app.system.menu_role.service.query_service import MenuRoleQueryService

router = APIRouter(tags=["System Menu Role"])
query_service = MenuRoleQueryService()
command_service = MenuRoleCommandService()


@router.get("/api/v1/admin/menu-roles", response_model=ApiResponse[list[MenuRoleResponse]],
            dependencies=[Depends(require_admin)])
async def get_all_menu_roles():
    return ApiResponse.ok(await query_service.get_all_menu_roles())


@router.put("/api/v1/admin/menu-roles/{role_id}", response_model=ApiResponse,
            dependencies=[Depends(require_admin)])
async def update_menu_roles(role_id: str, request: UpdateMenuRoleRequest,
                            user: CurrentUser = Depends(get_current_user)):
    await command_service.update_menu_roles(role_id, request.menu_ids, user.user_id)
    return ApiResponse.ok(None)
