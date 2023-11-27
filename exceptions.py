from fastapi import HTTPException, status
from jose import JWTError, jwt

class InternalServerException(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    self.detail = "Sometime went wrong"

class UnAuthorized(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_401_UNAUTHORIZED
    self.detail="Authentication is required to access this resource"

class PermissionDenied(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_403_FORBIDDEN
    self.detail="You don't have permission to perform this action"

class InvalidFormData(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    self.detail="Invalid form data"

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