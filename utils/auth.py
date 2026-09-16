from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import UserToken, User
from datetime import datetime
from fastapi import Header, Depends, HTTPException
from config.db_config import get_database
from starlette import status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_user_by_token(db: AsyncSession, token: str):
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    db_token = result.scalar() 
    if not db_token:
        return None
    if db_token.expires_at < datetime.now():
        return None
    stmt = select(User).where(User.id == db_token.user_id)
    result = await db.execute(stmt)
    return result.scalar()

async def get_current_user(
    authorization: str = Header(..., alias='Authorization'),
    db: AsyncSession = Depends(get_database)
):
    token = authorization
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, '无效的令牌或已经过期的令牌')
    return user