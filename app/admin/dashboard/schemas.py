from pydantic import BaseModel, Field


class AdminDashboardStatsResponse(BaseModel):
    total_users: int = Field(alias="totalUsers")
    today_registered: int = Field(alias="todayRegistered")
    active_boards: int = Field(alias="activeBoards")
    today_posts: int = Field(alias="todayPosts")
    model_config = {"populate_by_name": True}


class RecentUserResponse(BaseModel):
    id: str
    username: str
    name: str
    email: str | None = None
    created_at: str | None = Field(None, alias="createdAt")
    model_config = {"populate_by_name": True}
