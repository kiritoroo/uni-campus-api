from pydantic import BaseModel
from typing import Optional
from user.models import UserRoleModel
from fastapi import Form

class UserCreateSchema(BaseModel):
  username: str
  nickname: str
  hashed_pwd: str
  role: UserRoleModel
  
class UserCreateFormSchema(BaseModel):
  username: str
  nickname: str
  plain_pwd: str
  role: UserRoleModel
  
  def __init__(
    self,
    username: str = Form(...),
    nickname: str = Form(...),
    plain_pwd: str = Form(...),
    role: UserRoleModel = Form(...)
  ):
    return super().__init__(
      username=username,
      nickname=nickname,
      plain_pwd=plain_pwd,
      role=role
    )
