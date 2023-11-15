from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from core.db import campus_db
from core.log import logger
from service import PasswordService
from user.schemas import UserSignupFormSchema, UserSignupSchema, UserLoginFormSchema
from user.service import UserService
from user.models import UserModel
from typing_extensions import Annotated
from user.exceptions import IncorrectCredential
from dependencies import dp_pass_service

user_col = campus_db.get_collection("user")

async def dp_user_col() -> AsyncIOMotorCollection:
  yield user_col
  
async def dp_handle_signup(
  form: Annotated[UserSignupFormSchema, Depends()],
  pass_service: Annotated[PasswordService, Depends(dp_pass_service)]
) -> UserSignupSchema:
  try:
    hashed_pwd = await pass_service.hashed_password(plain_password=form.plain_pwd)
    schema = UserSignupSchema(
      username=form.username,
      nickname=form.nickname,
      hashed_pwd=hashed_pwd,
    )
    
    return schema
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid form data")

async def dp_handle_login(
  form: Annotated[UserLoginFormSchema, Depends()],
  pass_service: Annotated[PasswordService, Depends(dp_pass_service)],
  user_col: Annotated[AsyncIOMotorCollection, Depends(dp_user_col)]
) -> UserModel:
  if not (user := await UserService(user_col).get_user_by_username(form.username)) \
    or not await pass_service.verify_password(plain_password=form.plain_pwd, hashed_password=user.hashed_pwd):
    raise IncorrectCredential()
  
  return user
  