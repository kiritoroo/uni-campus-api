from pydantic import BaseModel, Field
from models import Vector3Model

class BuildingUpdateSchema(BaseModel):
  name: str = Field(...)
  space: str
  file_url: str
  uses: str
  position: Vector3Model
  rotation: Vector3Model
  scale: Vector3Model
  
class BuildingCreateSchema(BuildingUpdateSchema):
  pass
