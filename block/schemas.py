from pydantic import BaseModel, ConfigDict, Field
from fastapi import Form, File, UploadFile
from typing import Optional
from bson import ObjectId
from datetime import datetime

from models import Vector3Model, FileInfoModel, CoordinateModel, DBRefModel, PyObjectId
from space.models import SpaceModel

class BlockPopulateSchema(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: Optional[str] = None
  obj_name: Optional[str] = None
  building_id: Optional[PyObjectId] = None
  space: Optional[SpaceModel] = None
  uses: Optional[str] = None
  direction_url: Optional[str] = None
  coordinate: Optional[CoordinateModel] = None
  marker_position: Optional[Vector3Model] = None
  gallery: Optional[list[FileInfoModel]] = None
  is_public: Optional[bool] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(
    arbitrary_types_allowed=True,
  )

class BlockCreateSchema(BaseModel):
  name: str
  obj_name: str
  building_id: ObjectId
  space_id: ObjectId
  uses: str
  direction_url: str
  coordinate: CoordinateModel
  marker_position: Vector3Model
  gallery: list[FileInfoModel]
  
  model_config = ConfigDict(
    arbitrary_types_allowed=True,
  )

class BlockUpdateSchema(BaseModel):
  name: Optional[str]
  space_id: Optional[ObjectId]
  uses: Optional[str]
  direction_url: Optional[str]
  coordinate: Optional[CoordinateModel]
  marker_position: Optional[Vector3Model]
  gallery: Optional[list[FileInfoModel]]
  is_public: Optional[bool]

  model_config = ConfigDict(
    arbitrary_types_allowed=True,
  )

class BlockCreateFormSchema(BaseModel):
  name: str
  obj_name: str
  building_id: str
  space_id: str
  uses: str
  direction_url: str
  coordinate: str
  marker_position: str
  gallery: list[UploadFile]
  
  def __init__(
    self,
    name: str = Form(...),
    obj_name: str = Form(...),
    building_id: str = Form(...),
    space_id: str = Form(...),
    uses: str = Form(...),
    direction_url: str = Form(...),
    coordinate: str = Form(...),
    marker_position: str = Form(...),
    gallery: list[UploadFile] = list[File()]
  ):
    return super().__init__(
      name=name,
      obj_name=obj_name,
      building_id=building_id,
      space_id=space_id,
      uses=uses,
      direction_url=direction_url,
      coordinate=coordinate,
      marker_position=marker_position,
      gallery=gallery
    )
  
class BlockUpdateFormSchema(BaseModel):
  name: Optional[str]
  space_id: Optional[str]
  uses: Optional[str]
  direction_url: Optional[str]
  coordinate: Optional[str]
  marker_position: Optional[str]
  gallery: Optional[list[UploadFile]]
  is_public: Optional[bool]
  
  def __init__(
    self,
    name: str = Form(None),
    space_id: str = Form(None),
    uses: str = Form(None),
    direction_url: str = Form(None),
    coordinate: str = Form(None),
    marker_position: str = Form(None),
    gallery: list[UploadFile] = None,
    is_public: bool = Form(None)
  ):
    return super().__init__(
      name=name,
      space_id=space_id,
      uses=uses,
      direction_url=direction_url,
      coordinate=coordinate,
      marker_position=marker_position,
      gallery=gallery,
      is_public=is_public
    )