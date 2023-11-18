from pydantic import BaseModel, ConfigDict, Field
from fastapi import Form, File, UploadFile
from typing import Optional, List
from datetime import datetime

from models import Vector3Model, FileInfoModel, PyObjectId
from block.models import BlockModel

class BuildingPopulateSchema(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: str = None
  space_id: Optional[str] = None
  uses: Optional[str] = None
  position: Optional[Vector3Model] = None
  rotation: Optional[Vector3Model] = None
  scale: Optional[Vector3Model] = None
  model_3d: Optional[FileInfoModel] = None
  preview_img: Optional[FileInfoModel] = None
  is_public: Optional[bool] = None
  blocks: List[BlockModel]
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  
  model_config = ConfigDict(
    arbitrary_types_allowed=True
  )

class BuildingCreateSchema(BaseModel):
  name: str
  space_id: str
  uses: str
  position: Vector3Model
  rotation:  Vector3Model
  scale:  Vector3Model
  model_3d: FileInfoModel
  preview_img: FileInfoModel
  
class BuildingUpdateSchema(BaseModel):
  name: Optional[str]
  space_id: Optional[str]
  uses: Optional[str]
  position: Optional[Vector3Model]
  rotation:  Optional[Vector3Model]
  scale:  Optional[Vector3Model]
  model_3d: Optional[FileInfoModel]
  preview_img: Optional[FileInfoModel]
  is_public: Optional[bool]

class BuildingCreateFormSchema(BaseModel):
  name: str
  space_id: str
  uses: str
  position: str
  rotation:  str
  scale:  str
  model_file: UploadFile
  preview_file: UploadFile
  
  def __init__(
    self,
    name: str = Form(...),
    space_id: str = Form(...),
    uses: str = Form(...),
    position: str = Form(...),
    rotation: str = Form(...),
    scale:  str = Form(...),
    model_file: UploadFile = File(),
    preview_file: UploadFile = File()
  ):
    return super().__init__(
      name=name,
      space_id=space_id,
      uses=uses,
      position=position,
      rotation=rotation,
      scale=scale,
      model_file=model_file,
      preview_file=preview_file,
    )
    
class BuildingUpdateFormSchema(BaseModel):
  name: Optional[str]
  space_id: Optional[str]
  uses: Optional[str]
  position: Optional[str]
  rotation:  Optional[str]
  scale:  Optional[str]
  model_file: Optional[UploadFile]
  preview_file: Optional[UploadFile]
  is_public: Optional[bool]
  
  def __init__(
    self,
    name: str = Form(None),
    space_id: str = Form(None),
    uses: str = Form(None),
    position: str = Form(None),
    rotation: str = Form(None),
    scale:  str = Form(None),
    model_file: UploadFile = None,
    preview_file: UploadFile = None,
    is_public: bool = Form(None)
  ):
    return super().__init__(
      name=name,
      space_id=space_id,
      uses=uses,
      position=position,
      rotation=rotation,
      scale=scale,
      model_file=model_file,
      preview_file=preview_file,
      is_public=is_public
    )
    
