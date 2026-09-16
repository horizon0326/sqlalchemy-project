from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update
from models.history import History
from models.news import News
from datetime import datetime

async def add_news_history(db: AsyncSession, user_id: int, news_id: int):
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    history = result.scalar()
    if not history:
        favorite = History(user_id=user_id, news_id=news_id)
        db.add(favorite)
        await db.commit()
        return favorite

    stmt = update(History).where(History.user_id == user_id, History.news_id == news_id).values(view_time=datetime.now())
    await db.execute(stmt)
    await db.commit()
    return history
    
async def get_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()


    offset = (page - 1) * page_size
    query = (select(News, History.view_time)
            .join(History, History.news_id == News.id)
            .where(History.user_id == user_id)
            .order_by(History.view_time.desc())
            .offset(offset).limit(page_size)
            )
    result = await db.execute(query)
    rows = result.all()
    return rows, total

async def remove_news_history(db: AsyncSession, user_id: int, history_id: int):
    stmt = delete(History).where(History.user_id == user_id, History.news_id == history_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def reomve_all_history(db: AsyncSession, user_id: int):
    stmt = delete(History).where(History.user_id == user_id)
    await db.execute(stmt)
    await db.commit()