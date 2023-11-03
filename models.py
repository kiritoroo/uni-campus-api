from typing import Any
from typing import Annotated, Union
from bson import ObjectId
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema
from pydantic import BaseModel

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
