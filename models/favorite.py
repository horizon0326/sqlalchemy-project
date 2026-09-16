from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Index, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from models.users import User
from models.news import News

class Base(DeclarativeBase):
    pass

class Favorite(Base):
    __tablename__ = 'favorite'

    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),
        Index('fk_favorite_news_idx', 'news_id')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='收藏ID')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), comment='用户ID')
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), comment='新闻ID')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment='创建时间')