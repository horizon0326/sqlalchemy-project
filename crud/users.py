from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import uuid

async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar()
    return user

async def create_user(db: AsyncSession, user_data: UserRequest):
    hashed_pasword = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_pasword)
    db.add(user)
    await db.commit()
    return user

async def create_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(stmt)
    user_token = result.scalar()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user

async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_none=True,
        exclude_unset=True
    ))
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')

    update_user = await get_user_by_username(db, username)
    return update_user

async def change_password(db: AsyncSession, user: User, old_pasword: str, new_pasword: str):
    if not security.verify_password(old_pasword, user.password):
        return False

    hashed_now_pwd = security.get_hash_password(new_pasword)
    user.password = hashed_now_pwd
    await db.commit()
    return True