from fastapi import APIRouter, Depends, status

from app.common.schemas import ApiResponse
from app.security.dependencies import CurrentUser, get_current_user, require_admin
from app.system.menu.schemas import CreateMenuRequest, MenuResponse, MyMenusResponse, UpdateMenuRequest
from app.system.menu.service.command_service import MenuCommandService
from app.system.menu.service.query_service import MenuQueryService

router = APIRouter(tags=["System Menu"])
query_service = MenuQueryService()
command_service = MenuCommandService()


@router.get("/api/v1/admin/menus", response_model=ApiResponse[list[MenuResponse]], dependencies=[Depends(require_admin)])
async def get_menu_list():
    return ApiResponse.ok(await query_service.get_all_menus())


@router.get("/api/v1/menus/my", response_model=ApiResponse[MyMenusResponse])
async def get_my_menus(current_user: CurrentUser = Depends(get_current_user)):
    menus = await query_service.get_menus_by_role_ids(current_user.roles)
    admin_menus = await query_service.get_admin_menus() if current_user.is_admin else []
    return ApiResponse.ok(MyMenusResponse(menus=menus, admin_menus=admin_menus))


@router.post("/api/v1/admin/menus", response_model=ApiResponse[list[MenuResponse]],
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_menu(request: CreateMenuRequest, user: CurrentUser = Depends(get_current_user)):
    await command_service.create_menu(
        request.id, request.name, request.path, request.icon, request.parent_id, request.sort_order, user.user_id
    )
    return ApiResponse.ok(await query_service.get_all_menus())


@router.put("/api/v1/admin/menus/{menu_id}", response_model=ApiResponse[list[MenuResponse]],
            dependencies=[Depends(require_admin)])
async def update_menu(menu_id: str, request: UpdateMenuRequest, user: CurrentUser = Depends(get_current_user)):
    await command_service.update_menu(
        menu_id, request.name, request.path, request.icon, request.parent_id, request.sort_order, user.user_id
    )
    return ApiResponse.ok(await query_service.get_all_menus())


@router.delete("/api/v1/admin/menus/{menu_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_admin)])
async def delete_menu(menu_id: str):
    await command_service.delete_menu(menu_id)
