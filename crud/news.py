from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News
from cache.news_cache import get_cache_categories, set_cache_categories
from fastapi.encoders import jsonable_encoder
from cache.news_cache import get_cache_news_list, set_cache_news_list

async def get_categories(db: AsyncSession, skip: int=0, limit: int=100):
    cached_categories = await get_cache_categories()
    if cached_categories:
        return cached_categories
        
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)
        
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    page = skip // limit + 1
    cache_list = await get_cache_news_list(category_id, page, limit)
    if cache_list:
        return cache_list
        
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    if news_list:
        news_list = jsonable_encoder(news_list)
        await set_cache_news_list(category_id, page, limit, news_list)
        
    return news_list

async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    count = result.scalar()
    return count

async def get_new_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    detail = result.scalar()
    return detail

async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount > 0

async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id,
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)

    result = await db.execute(stmt)
    related = result.scalars().all()
    return related