from pydantic import BaseModel, Field, ConfigDict
from models import PyObjectId
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  username: Optional[str] = None
  nickname: Optional[str] = None
  hashed_pwd: Optional[str] = None
  role: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  last_login: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "id": "some_id",
        "username": "some_username",
        "nickname": "some_nickname",
        "role": "some_role",
        "hashed_pwd": "some_hashed_password",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
      }
    }
  )

class TokenResponseModel(BaseModel):
  token: Optional[str] = None

  model_config = ConfigDict(
    populate_by_name=True,
    protected_namespaces=('token_model_'),
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "token": "some_token",
      }
    }
  )