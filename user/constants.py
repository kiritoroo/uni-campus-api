from enum import Enum
from fastapi import status
from user.models import TokenResponseModel

class UserRole(str, Enum):
  GUEST = "guest"
  ADMIN = "admin"
  SUPERADMIN = "superadmin"

class TokenType(str, Enum):
  ACCESS_TOKEN = 'access_token'
  REFRESH_TOKEN = 'refresh_token'
  
SIGNUP_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_201_CREATED,
  'description': "User Signup",
  'response_description': "Returns authentication tokens.",
  'response_model': TokenResponseModel,
}