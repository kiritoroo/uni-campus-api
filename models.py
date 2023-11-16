from typing import Any
from typing import Annotated, Union, Optional
from bson import ObjectId
from pydantic import BaseModel, PlainSerializer, AfterValidator, WithJsonSchema, model_validator, ConfigDict
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