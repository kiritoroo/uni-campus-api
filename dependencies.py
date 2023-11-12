from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing_extensions import Annotated
from service import PasswordService, TokenService
from passlib.context import CryptContext
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from bson import ObjectId
from exceptions import UnAuthorized
import os

security = HTTPBearer()

async def dp_pass_service() -> PasswordService:
  return PasswordService(CryptContext(schemes=['bcrypt'], deprecated='auto'))

async def dp_token_service() -> TokenService:
  return TokenService()


async def dp_auth(
  credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
  dp_token_service: Annotated[TokenService, Depends(dp_token_service)]
) -> bool:
  try:
    token_encrypt = credentials.credentials
    aes_key = os.environ.get('AES_KEY')
    cbc_iv = os.environ.get('CBC_IV')
    
    token_encrypt_bytes = b64decode(token_encrypt)
    aes_key_bytes = aes_key.encode('utf-8')
    cbc_iv_bytes = cbc_iv.encode('utf-8')
    
    cipher = AES.new(key=aes_key_bytes, mode=AES.MODE_CBC, iv=cbc_iv_bytes)
    token_bytes = unpad(cipher.decrypt(token_encrypt_bytes), AES.block_size, style='pkcs7')
    token = b64decode(b64encode(token_bytes)).decode('ascii')
    
    claims = await dp_token_service.decode_access_token(
      token,
      secret_key=os.environ.get('SECRET_KEY'),
      algorithm=os.environ.get('ALGORITHM')
    )
    
    if not claims or not ObjectId.is_valid(claims['user_id']):
      raise UnAuthorized()

    return True
  except Exception as e:
    raise UnAuthorized()
    