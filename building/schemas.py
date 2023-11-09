from pydantic import BaseModel, Field, model_validator, create_model
from models import Vector3Model, FileInfoModel
from fastapi import Form, File, UploadFile
from core.log import logger
from dataclasses import dataclass
from typing import Optional
import json

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
  name: str
  space_id: str
  uses: str
  position: Vector3Model
  rotation:  Vector3Model
  scale:  Vector3Model
  model_3d: Optional[FileInfoModel]
  preview_img: Optional[FileInfoModel]

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
  name: str
  space_id: str
  uses: str
  position: str
  rotation:  str
  scale:  str
  model_file: Optional[UploadFile] = None
  preview_file: Optional[UploadFile] = None
  
  def __init__(
    self,
    name: str = Form(...),
    space_id: str = Form(...),
    uses: str = Form(...),
    position: str = Form(...),
    rotation: str = Form(...),
    scale:  str = Form(...),
    model_file: Optional[UploadFile] = None,
    preview_file: Optional[UploadFile] = None
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
    
