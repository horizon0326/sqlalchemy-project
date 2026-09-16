from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Index, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from models.users import User
from models.news import News

class Base(DeclarativeBase):
    pass

class History(Base):
    __tablename__ = 'history'

    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='浏览ID')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), comment='用户ID')
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), comment='新闻ID')
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment='浏览时间')

    def __repr__(self):
        return f"<History(id='{self.id}', user_id='{self.user_id}', news_id='{self.news_id}, view_time='{self.view_time}')>"