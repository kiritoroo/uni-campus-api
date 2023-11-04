from pydantic import BaseModel, Field
from typing import Optional
from models import Vector3Model

class BuildingCreateSchema(BaseModel):
  name: str = Field(...)
  space: str
  file_buffer: str
  uses: str
  position: Vector3Model
  rotation: Vector3Model
  scale: Vector3Model
  