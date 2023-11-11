from fastapi import APIRouter, Depends, Response, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from typing_extensions import Annotated
from user.schemas import UserCreateFormSchema, UserCreateSchema
from user.dependencies import dp_user_col, dp_handle_signup, dp_token_service
from user.service import UserService, TokenService
from user.exceptions import UserExists
from core.log import logger
import user.constants as cst
import os
import json

user_router = APIRouter(prefix='/user', tags=['User'])

@user_router.post('/signup', **cst.SIGNUP_ENDPOINT_DEFINITION)
async def signup(
  form: Annotated[UserCreateFormSchema, Depends()],
  user_signup_data: Annotated[UserCreateSchema, Depends(dp_handle_signup)],
  dp_token_service: Annotated[TokenService, Depends(dp_token_service)],
  user_col: Annotated[AsyncIOMotorCollection, Depends(dp_user_col)]
):
  exists_user = await UserService(user_col).get_user_by_username(user_signup_data.username)
  if exists_user:
    raise UserExists()
    
  res_user = await UserService(user_col).create_user(user_signup_data)
  token = await dp_token_service.encode_token(
    user_id=str(res_user.id),
    username=res_user.username,
    nickname=res_user.nickname,
    role=res_user.role,
    secret_key=os.environ.get('SECRET_KEY'),
    algorithm=os.environ.get('ALGORITHM'),
    exp_time=int(os.environ.get('EXP_TIME')),
    token_type=cst.TokenType.ACCESS_TOKEN
  )
  
  res_json = json.dumps(dict({'access_token': token}))
  logger.debug(res_json)

  return Response(
    content=res_json,
    status_code=status.HTTP_201_CREATED,
  )
  
@user_router.post('/login')
async def login(
  
):
  pass