from typing import Any
from typing import Annotated, Union, Optional, Dict
from bson import ObjectId
from pydantic import BaseModel, PlainSerializer, AfterValidator, WithJsonSchema, model_validator, ConfigDict, model_serializer
from constants import TokenType
from datetime import datetime
import json

def validate_object_id(v: Any) -> ObjectId:
  if isinstance(v, ObjectId):
      return v
  if ObjectId.is_valid(v):
      return ObjectId(v)
  raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[
  Union[str, ObjectId],
  AfterValidator(validate_object_id),
  PlainSerializer(lambda x: str(x), return_type=str),
  WithJsonSchema({"type": "string"}, mode="serialization"),
]

class ClaimsModel(BaseModel):
  user_id: str
  username: str
  nickname: str
  role: str
  exp: datetime
  iat: datetime
  token_type: TokenType

  class Config:
      allow_population_by_field_name = True


class Vector3Model(BaseModel):
  x: float
  y: float
  z: float

  @model_validator(mode='before')
  @classmethod
  def validate_to_json(cls, value):
    if isinstance(value, str):
      return cls(**json.loads(value))
    return value
  
class CoordinateModel(BaseModel):
  latitude: float
  longitude: float

  @model_validator(mode='before')
  @classmethod
  def validate_to_json(cls, value):
    if isinstance(value, str):
      return cls(**json.loads(value))
    return value
  
class DBRefModel(BaseModel):
  ref: str
  id: str
  
  @model_serializer
  def ser_model(self) -> Dict[str, Any]:
    return {
      '$ref': self.ref,
      '$id': ObjectId(self.id)
    }
  
class FileInfoModel(BaseModel):
  id: str
  url: str
  filename: str
  extension: str
  length: float
  content_type: str
  
  @model_validator(mode='before')
  @classmethod
  def validate_to_json(cls, value):
    if isinstance(value, str):
      return cls(**json.loads(value))
    return value

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