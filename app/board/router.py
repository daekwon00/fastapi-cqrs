from fastapi import APIRouter, Depends, Query, status

from app.board.schemas import (
    BoardResponse,
    CreatePostRequest,
    PostListResponse,
    PostResponse,
    UpdatePostRequest,
)
from app.board.service.command_service import PostCommandService
from app.board.service.query_service import BoardQueryService, PostQueryService
from app.common.pagination import PagingParams, SortOrder
from app.common.schemas import ApiResponse, PageResponse
from app.security.dependencies import CurrentUser, get_current_user

router = APIRouter(tags=["Board"])
board_query_service = BoardQueryService()
post_query_service = PostQueryService()
post_command_service = PostCommandService()


@router.get("/api/v1/boards", response_model=ApiResponse[list[BoardResponse]])
async def get_board_list():
    result = await board_query_service.get_board_list()
    return ApiResponse.ok(result)


@router.get("/api/v1/boards/{board_id}", response_model=ApiResponse[BoardResponse])
async def get_board_by_id(board_id: str):
    result = await board_query_service.get_board_by_id(board_id)
    return ApiResponse.ok(result)


@router.get("/api/v1/boards/{board_id}/posts", response_model=ApiResponse[PageResponse[PostListResponse]])
async def get_post_list(
    board_id: str,
    paging: PagingParams = Depends(),
    search: str | None = Query(None, description="검색어"),
    search_type: str | None = Query("all", alias="searchType", description="검색 타입 (title, author, all)"),
):
    content = await post_query_service.get_post_list(
        board_id, search, search_type, paging.sort_order, paging.limit, paging.offset
    )
    total = await post_query_service.get_post_count(board_id, search, search_type)
    return ApiResponse.ok(PageResponse.of(content, total, paging.page, paging.size))


@router.get("/api/v1/posts/recent", response_model=ApiResponse[list[PostListResponse]])
async def get_recent_posts():
    result = await post_query_service.get_recent_posts()
    return ApiResponse.ok(result)


@router.get("/api/v1/posts/{post_id}", response_model=ApiResponse[PostResponse])
async def get_post_detail(post_id: int):
    await post_command_service.increase_view_count(post_id)
    result = await post_query_service.get_post_detail(post_id)
    return ApiResponse.ok(result)


@router.post("/api/v1/posts", response_model=ApiResponse[PostResponse], status_code=status.HTTP_201_CREATED)
async def create_post(
    request: CreatePostRequest,
    current_user: CurrentUser = Depends(get_current_user),
):
    result = await post_command_service.create_post(
        request.board_id, request.title, request.content, current_user.user_id, request.file_ids
    )
    return ApiResponse.ok(result)


@router.put("/api/v1/posts/{post_id}", response_model=ApiResponse[PostResponse])
async def update_post(
    post_id: int,
    request: UpdatePostRequest,
    current_user: CurrentUser = Depends(get_current_user),
):
    result = await post_command_service.update_post(
        post_id, request.title, request.content, current_user.user_id, request.file_ids
    )
    return ApiResponse.ok(result)


@router.delete("/api/v1/posts/{post_id}", response_model=ApiResponse)
async def delete_post(
    post_id: int,
    current_user: CurrentUser = Depends(get_current_user),
):
    await post_command_service.delete_post(post_id)
    return ApiResponse.ok()
