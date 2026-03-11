from pydantic import Field

from app.common.schemas import CamelModel


class AdminDashboardStatsResponse(CamelModel):
    total_users: int = Field(alias="totalUsers")
    today_registered: int = Field(alias="todayRegistered")
    active_boards: int = Field(alias="activeBoards")
    today_posts: int = Field(alias="todayPosts")


class RecentUserResponse(CamelModel):
    id: str
    username: str
    name: str
    email: str | None = None
    created_at: str | None = Field(None, alias="createdAt")
