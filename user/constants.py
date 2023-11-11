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
  'response_description': "Return authentication tokens",
  'response_model': TokenResponseModel,
}

LOGIN_ENDPOINT_DEFINITION = {
  'status_code': status.HTTP_200_OK,
  'description': "User Login",
  'response_description': "Return authentication tokens",
  'response_model': TokenResponseModel,
}