from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_database
from schemas.users import UserRequest
from schemas.users import UserAuthResponse, UserInfoResponse, ResponseModel, UserUpdateRequest, UserChangePasswordRequest
from starlette import status
from crud import users
from models.users import User
from utils.auth import get_current_user

router = APIRouter(prefix='/api/user', tags=['用户'])

@router.post('/register', response_model=ResponseModel)
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_database)):
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, '用户已存在')
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return ResponseModel(message='注册成功', data=response_data)

@router.post('/login', response_model=ResponseModel)
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_database)):
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, '用户名或密码错误')
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return ResponseModel(message='登录成功', data=response_data)

@router.get('/info', response_model=ResponseModel)
async def get_user_info(user: User = Depends(get_current_user)):
    return ResponseModel(message='获取用户信息成功', data=UserInfoResponse.model_validate(user))

@router.put('/update')
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_database)):
    user = await users.update_user(db, user.username, user_data)
    return ResponseModel(message='登录成功', data=UserInfoResponse.model_validate(user))

@router.put('/password')
async def update_password(
    password_data: UserChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    res_change_pwd = await users.change_password(db, user, password_data.old_pasword, password_data.new_pasword)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='修改密码失败')
    return ResponseModel(message='修改密码成功')