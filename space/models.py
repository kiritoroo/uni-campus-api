from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from pydantic.color import Color
from datetime import datetime

from models import PyObjectId, FileInfoModel


class SpaceModel(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: Optional[str] = None
  color: Optional[str] = None
  icon: Optional[FileInfoModel] = None
  order: Optional[int] = None
  slug: Optional[str] = None
  is_publish: Optional[bool] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    protected_namespaces=('space_model_'),
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "id": "some_id",
        "name": "Your Space Name",
        "color": "#fff",
        "icon": {"id": "file_id", "url": "file_url", "filename": "file_name", "extension": "file_extension", "length": 12345, "content_type": "image/png"},
        "is_publish": True,
        "created_at": "2023-11-03T10:00:00",
        "updated_at": "2023-11-03T10:00:00"
      }
    }
  )
