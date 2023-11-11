from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from core.db import campus_db
from core.log import logger
from user.schemas import UserCreateFormSchema, UserCreateSchema
from user.service import PasswordService, TokenService
from typing_extensions import Annotated
from passlib.context import CryptContext

user_col = campus_db.get_collection("user")

async def dp_user_col() -> AsyncIOMotorCollection:
  yield user_col
  
async def dp_pass_service() -> PasswordService:
  return PasswordService(CryptContext(schemes=['bcrypt'], deprecated='auto'))

async def dp_token_service() -> TokenService:
  return TokenService()

async def dp_handle_signup(
  form: Annotated[UserCreateFormSchema, Depends()],
  pass_service: Annotated[PasswordService, Depends(dp_pass_service)]
) -> UserCreateSchema:
  try:
    hashed_pwd = await pass_service.hashed_password(plain_password=form.plain_pwd)
    schema = UserCreateSchema(
      username=form.username,
      nickname=form.nickname,
      hashed_pwd=hashed_pwd,
      role=form.role.value
    )
    
    return schema
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid form data")
