from fastapi import HTTPException, status

class UserNotFound(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_404_NOT_FOUND
    self.detail = "User not found"
    
class UserExists(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_400_BAD_REQUEST
    self.detail="Username already registered"

class IncorrectCredential(HTTPException):
  def __init__(self):
    self.status_code = status.HTTP_401_UNAUTHORIZED
    self.detail="Incorrect username or password"
