from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models import PyObjectId, FileInfoModel
from pydantic.color import Color
from datetime import datetime

class SpaceModel(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: Optional[str] = None
  color: Optional[Color] = None
  icon: Optional[FileInfoModel] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  class Config:
    json_encoders = {
      Color: lambda x: x.as_hex()
    }
  
  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "id": "some_id",
        "name": "Your Space Name",
        "icon": {"id": "file_id", "url": "file_url", "filename": "file_name", "extension": "file_extension", "length": 12345, "content_type": "image/png"}
      }
    }
  )