from exceptions import token_exception
from passlib.context import CryptContext
from constants import TokenType
from models import ClaimsModel
from jose import jwt
from datetime import datetime, timedelta

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
  async def decode_access_token(self, access_token: str, secret_key: str, algorithm: str) -> ClaimsModel:
    claims = ClaimsModel(
      *jwt.decode(
        token=access_token,
        key=secret_key,
        algorithms=algorithm
      )
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
    expire_time = datetime.utcnow() + timedelta(days=exp_time)
    issued_at = datetime.utcnow()
    claims = ClaimsModel(
      user_id=user_id,
      username=username,
      nickname=nickname,
      role=role,
      exp=expire_time,
      iat=issued_at,
      token_type=token_type.value
    )
    return jwt.encode(claims.model_dump(), key=secret_key, algorithm=algorithm)
