from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Text, Index, ForeignKey
from typing import Optional

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment='创建时间'
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment='创建时间'
    )

class Category(Base):
    __tablename__ = 'news_category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='分类ID')
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='分类名称')
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment='排序')
    
    def __repr__(self):
        return f"<Category(id='{self.id}', name='{self.name}', sort_order='{self.sort_order}')>"

class News(Base):
    __tablename__ = 'news'

    __table_args__ = (
        Index('fk_new_category_idx', "category_id"),
        Index('idx_publish_time', 'publish_time')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='新闻ID')
    title: Mapped[str] = mapped_column(String(255), comment='新闻标题')
    description: Mapped[Optional[str]] = mapped_column(String(500), comment='新闻简介')
    content: Mapped[str] = mapped_column(Text, comment='新闻内容')
    image: Mapped[Optional[str]] = mapped_column(String(255), comment='新闻图片URL')
    author: Mapped[Optional[str]] = mapped_column(String(50), comment='作者')
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), comment='分类ID')
    views: Mapped[int] = mapped_column(Integer, default=0, comment='浏览量')
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment='发布时间')

    def __repr__(self):
        return f"<News(id='{self.id}', title='{self.title}', views='{self.views}')>"