from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Generic, TypeVar

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description='昵称')
    avatar: Optional[str] = Field(None, max_length=255, description='头像URL')
    gender: Optional[str] = Field(None, max_length=10, description='性别')
    bio: Optional[str] = Field(None, max_length=500, description='个人简介')

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )

class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias='userInfo')

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    code: int = 200
    message: str = 'success'
    data: Optional[T] = None
    
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None)
    avatar: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    
class UserChangePasswordRequest(BaseModel):
    old_pasword: str = Field(alias='oldPassword', description='旧密码')
    new_pasword: str = Field(alias='newPassword', min_length=6, description='新密码')