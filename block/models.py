from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from bson.dbref import DBRef

from models import PyObjectId, Vector3Model, FileInfoModel, CoordinateModel, DBRefModel


class BlockModel(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: Optional[str] = None
  obj_name: Optional[str] = None
  building_id: Optional[PyObjectId] = None
  space_id: Optional[PyObjectId] = None
  uses: Optional[str] = None
  direction_url: Optional[str] = None
  coordinate: Optional[CoordinateModel] = None
  marker_position: Optional[Vector3Model] = None
  gallery: Optional[list[FileInfoModel]] = None
  order: Optional[int] = None
  is_publish: Optional[bool] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    protected_namespaces=('block_model_'),
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "id": "65462fa907344798a6a7b4bf",
        "name": "Building Center",
        "obj_name": "Building Object",
        "uses": "Multi purpose",
        "space_id": "65462fa907344798a6a7b4bf",
        "building_id": "65462fa907344798a6a7b4bf", 
        "direction_url": "https://maps.google.com", 
        "coordinate": {"latitude": 0.0, "longitude": 0.0},
        "marker_position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "gallery": [
          {"file_name": "abc.jpg", "url": "abc.jpg", "extension": ".jpg", "length": 100, "content_type": "image/jpeg"},
          {"file_name": "123.jpg", "url": "123.jpg", "extension": ".jpg", "length": 100, "content_type": "image/jpeg"}
        ],
        "is_publish": True,
        "created_at": "2023-11-03T10:00:00",
        "updated_at": "2023-11-03T10:00:00",
      }
  },
)