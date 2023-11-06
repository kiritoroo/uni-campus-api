from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models import PyObjectId, Vector3Model
from datetime import datetime

class BuildingModel(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: str = Field(..., title="Building name")
  space_id: Optional[str] = None
  uses: Optional[str] = None
  model_url: Optional[str] = None
  preview_url: Optional[str] = None
  position: Optional[Vector3Model] = None
  rotation: Optional[Vector3Model] = None
  scale: Optional[Vector3Model] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "id": "65462fa907344798a6a7b4bf",
        "name": "Building Center",
        "space_id": "Office",
        "uses": "Multi purpose",
        "model_url": "aws s3",
        "preview_url": "aws s3",
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
        "scale": {"x": 0.0, "y": 0.0, "z": 0.0},
        "created_at": "2023-11-03T10:00:00",
        "updated_at": "2023-11-03T10:00:00"
      }
    },
)