from fastapi import HTTPException, status
from jose import JWTError, jwt

class UserNotFound(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_404_NOT_FOUND
    self.detail = "User not found"
    
class UserExists(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_400_BAD_REQUEST
    self.detail="Username already registered"
    
def token_exception(token_type: str, error_detail: str, headers: dict = None):
  def decorator(func):
    async def wrapper(*args, **kwargs):
      try:
        return await func(*args, **kwargs)
      except jwt.ExpiredSignatureError:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail=f'{token_type.capitalize()} expired')
      except JWTError:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail=error_detail, headers=headers)
    return wrapper
  return decorator