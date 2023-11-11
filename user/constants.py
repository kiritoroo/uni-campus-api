from enum import Enum

class UserRole(str, Enum):
  GUEST = "guest"
  ADMIN = "admin"
  SUPERADMIN = "superadmin"
  
class TokenType(str, Enum):
  ACCESS_TOKEN = 'access_token'
  REFRESH_TOKEN = 'refresh_token'