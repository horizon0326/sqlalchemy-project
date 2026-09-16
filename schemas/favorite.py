from pydantic import BaseModel, Field, ConfigDict
from .base import NewsItemBase
from datetime import datetime

class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias='isFavorite')

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias='newsId', ge=1)

class FavoriteAddResponse(BaseModel):
    user_id: int = Field(alias='userId')
    news_id: int = Field(alias='newsId')

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias='favoriteId')
    favorite_time: datetime = Field(alias='favoriteTime')

class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias='hasMore')

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )