from pydantic import BaseModel
from pydantic.color import Color
from models import FileInfoModel
from typing import Optional
from fastapi import Form, File, UploadFile

class SpaceCreateSchema(BaseModel):
  name: str
  color: str
  icon: FileInfoModel
  
class SpaceUpdateSchema(BaseModel):
  name: str
  color: str
  icon: Optional[FileInfoModel]
  is_public: bool

class SpaceCreateFormSchema(BaseModel):
  name: str
  color: Color
  icon_file: UploadFile
  
  def __init__(
    self,
    name: str = Form(...),
    color: Color = Form(...),
    icon_file: UploadFile = File(),
  ):
    return super().__init__(
      name=name,
      color=color,
      icon_file=icon_file
    )

class SpaceUpdateFormSchema(BaseModel):
  name: str
  color: Color
  icon_file: Optional[UploadFile] = None,
  is_public: bool
  
  def __init__(
    self,
    name: str = Form(...),
    color: Color = Form(...),
    icon_file: Optional[UploadFile] = None,
    is_public: bool = Form(...)
  ):
    return super().__init__(
      name=name,
      color=color,
      icon_file=icon_file,
      is_public=is_public
    )
