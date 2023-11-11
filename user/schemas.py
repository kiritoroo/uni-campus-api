from pydantic import BaseModel
from typing import Optional
from fastapi import Form
from user.constants import UserRole

class UserSignupSchema(BaseModel):
  username: str
  nickname: str
  hashed_pwd: str
  role: str

class UserSignupFormSchema(BaseModel):
  username: str
  nickname: str
  plain_pwd: str
  role: UserRole
  
  def __init__( self,
    username: str = Form(...),
    nickname: str = Form(...),
    plain_pwd: str = Form(...),
    role: UserRole = Form(...)
  ):
    return super().__init__(
      username=username,
      nickname=nickname,
      plain_pwd=plain_pwd,
      role=role
    )

class UserLoginFormSchema(BaseModel):
  username: str
  plain_pwd: str
  
  def __init__( self,
    username: str = Form(...),
    plain_pwd: str = Form(...),
  ):
    return super().__init__(
      username=username,
      plain_pwd=plain_pwd,
    )
