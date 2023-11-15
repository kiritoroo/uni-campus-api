from fastapi import APIRouter, Depends, Response, status
from motor.motor_asyncio import AsyncIOMotorCollection
from typing_extensions import Annotated
from user.schemas import UserSignupFormSchema, UserSignupSchema, UserLoginFormSchema
from user.dependencies import dp_user_col, dp_handle_signup, dp_handle_login
from user.service import UserService
from user.exceptions import UserExists
from user.models import UserModel
from core.log import logger
from constants import TokenType
from dependencies import dp_token_service
from service import TokenService
import user.constants as cst
from dependencies import dp_auth
import os
import json

user_router = APIRouter(prefix='/user', tags=['User'])

@user_router.post('/signup', **cst.SIGNUP_ENDPOINT_DEFINITION)
async def signup(
  auth: Annotated[bool, Depends(dp_auth)],
  form: Annotated[UserSignupFormSchema, Depends()],
  user_signup_data: Annotated[UserSignupSchema, Depends(dp_handle_signup)],
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
    token_type=TokenType.ACCESS_TOKEN
  )
  
  res_json = json.dumps(dict({'access_token': token}))
  logger.debug(res_json)

  return Response(
    content=res_json,
    status_code=status.HTTP_201_CREATED,
  )
  
@user_router.post('/login', **cst.LOGIN_ENDPOINT_DEFINITION)
async def login(
  form: Annotated[UserLoginFormSchema, Depends()],
  user_login_data: Annotated[UserModel, Depends(dp_handle_login)],
  dp_token_service: Annotated[TokenService, Depends(dp_token_service)],
  user_col: Annotated[AsyncIOMotorCollection, Depends(dp_user_col)]
):
  token = await dp_token_service.encode_token(
    user_id=str(user_login_data.id),
    username=user_login_data.username,
    nickname=user_login_data.nickname,
    role=user_login_data.role,
    secret_key=os.environ.get('SECRET_KEY'),
    algorithm=os.environ.get('ALGORITHM'),
    exp_time=int(os.environ.get('EXP_TIME')),
    token_type=TokenType.ACCESS_TOKEN
  )
  
  res_json = json.dumps(dict({'access_token': token}))
  logger.debug(res_json)

  return Response(
    content=res_json,
    status_code=status.HTTP_201_CREATED,
  )
