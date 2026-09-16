from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from .base import NewsItemBase

class HistoryAddRequest(BaseModel):
    news_id: int = Field(alias='newsId', ge=1)

class HistoryAddResponse(BaseModel):
    id: int
    user_id: int = Field(alias='userId')
    news_id: int = Field(alias='newsId')
    view_time: datetime = Field(alias='viewTime')

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryNewsItemResponse(NewsItemBase):
    view_time: datetime = Field(alias='viewTime')

class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias='hasMore')

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )