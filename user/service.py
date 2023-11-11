from passlib.context import CryptContext
from user.constants import TokenType
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from user.models import UserModel
from user.schemas import UserSignupSchema
from bson import ObjectId
from user.exceptions import token_exception, UserNotFound

class PasswordService():
  def __init__(self, _crypt_context: CryptContext) -> None:
    self.crypt_context = _crypt_context
    
  async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
    return self.crypt_context.verify_and_update(secret=plain_password, hash=hashed_password)[0]

  async def hashed_password(self, plain_password: str) -> str:
    return self.crypt_context.hash(secret=plain_password)

class TokenService():
  @token_exception(
    token_type='access_token',
    error_detail='Could not validate credentials'
  )
  async def decode_access_token(self, access_token: str, secret_key: str, algorithm: str) -> dict:
    claims: dict = jwt.decode(
      token=access_token,
      key=secret_key,
      algorithms=algorithm
    )
    if claims.get('token_type') == TokenType.ACCESS_TOKEN.value:
      return claims

  @token_exception(
    token_type='refresh_token',
    error_detail='Invalid refresh token'
  )
  async def decode_refresh_token(self, refresh_token: str, secret_key: str, algorithm: str) -> dict:
    claims: dict = jwt.decode(
      token=refresh_token,
      key=secret_key,
      algorithms=algorithm
    )
    if claims.get('token_type') == TokenType.REFRESH_TOKEN.value:
      return claims

  async def encode_token(self, user_id: str, username: str, nickname: str, role: str, secret_key: str, algorithm: str, exp_time: int, token_type: TokenType) -> str:
    expire_time = datetime.utcnow() + timedelta(minutes=exp_time)
    issued_at = datetime.utcnow()
    data = {
      'id': user_id,
      'username': username,
      'nickname': nickname,
      'role': role,
      'exp': expire_time,
      'iat': issued_at,
      'token_type': token_type.value
    }
    return jwt.encode(data, key=secret_key, algorithm=algorithm)

class UserService:
  def __init__(self, _user_col: AsyncIOMotorCollection):
    self.user_col = _user_col
    
  async def get_user_by_username(self, username: str) -> UserModel | None:
    query = {
      'filter': {
        'username': username
      }
    }
    
    user_raw = await self.user_col.find_one(**query)
    return UserModel(**user_raw) if user_raw else None
  
  async def get_user_by_id(self, id: str) -> UserModel:
    if not ObjectId.is_valid(id):
      raise UserNotFound()
    
    query = {
      'filter': {
        '_id': ObjectId(id)
      }
    }
    user_raw = await self.user_col.find_one(**query)
    
    if not user_raw:
      raise UserNotFound()
    
    user = UserModel(**user_raw)
    return user
  
  async def create_user(self, data: UserSignupSchema) -> UserModel:
    create_data = dict(
      **data.model_dump(exclude_none=True),
      created_at=datetime.utcnow(),
      updated_at=datetime.utcnow(),
      last_login=None
    )
    result = await self.user_col.insert_one(document=create_data)
    user = UserModel(id=result.inserted_id, **create_data)
    return user