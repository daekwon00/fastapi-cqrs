from fastapi import APIRouter, Depends

from app.common.schemas import ApiResponse
from app.security.dependencies import CurrentUser, get_current_user, require_admin
from app.system.position_role.schemas import PositionRoleResponse, UpdatePositionRoleRequest
from app.system.position_role.service.command_service import PositionRoleCommandService
from app.system.position_role.service.query_service import PositionRoleQueryService

router = APIRouter(tags=["System Position Role"])
query_service = PositionRoleQueryService()
command_service = PositionRoleCommandService()


@router.get("/api/v1/admin/position-roles", response_model=ApiResponse[list[PositionRoleResponse]],
            dependencies=[Depends(require_admin)])
async def get_all_position_roles():
    return ApiResponse.ok(await query_service.get_all_position_roles())


@router.put("/api/v1/admin/position-roles/{position_id}", response_model=ApiResponse,
            dependencies=[Depends(require_admin)])
async def update_position_roles(position_id: str, request: UpdatePositionRoleRequest,
                                user: CurrentUser = Depends(get_current_user)):
    await command_service.update_position_roles(position_id, request.role_ids, user.user_id)
    return ApiResponse.ok(None)
