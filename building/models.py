from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models import PyObjectId, Vector3Model

class BuildingModel(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: str = Field(...)
  space: Optional[str] = None
  model_buffer: Optional[bytes] = None
  uses: Optional[str] = None
  position: Optional[Vector3Model] = None
  rotation: Optional[Vector3Model] = None
  scale: Optional[Vector3Model] = None

  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "id": "65454e11fb75a3926d6c790d",
        "name": "Building Center",
        "space": "Office",
        "model_buffer": b'\x00\x00\x00\x00\x00',
        "uses": "Multi purpose",
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
        "scale": {"x": 0.0, "y": 0.0, "z": 0.0}
      }
    },
)