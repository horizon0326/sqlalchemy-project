from fastapi import APIRouter, Depends, Query, HTTPException, status
from schemas.history import HistoryAddRequest, HistoryAddResponse
from models.users import User
from utils.auth import get_current_user
from config.db_config import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from crud import history
from schemas.users import ResponseModel
from schemas.history import HistoryListResponse

router = APIRouter(prefix='/api/history', tags=['浏览'])

@router.post('/add')
async def add_history(data: HistoryAddRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_database)):
    result = await history.add_news_history(db, user.id, data.news_id)
    return ResponseModel(message='添加浏览记录成功', data=HistoryAddResponse.model_validate(result))

@router.get('/list')
async def get_history_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=10, alias='pageSize'),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    rows, total = await history.get_history_list(db, user.id, page, page_size)
    history_list = [{**history.__dict__, 'view_time': view_time} for history, view_time in rows]
    has_more = total > page * page_size
    data = HistoryListResponse(list=history_list, total=total, has_more=has_more)
    return ResponseModel(message='获取浏览记录成功', data=data)

@router.delete('/delete/{history_id}')
async def delete_history(history_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_database)):
    result = await history.remove_news_history(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='浏览记录不存在')
    return ResponseModel(message='删除浏览记录成功')

@router.delete('/clear')
async def clear_history(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_database)):
    await history.reomve_all_history(db, user.id)
    return ResponseModel(message='清空浏览记录成功')