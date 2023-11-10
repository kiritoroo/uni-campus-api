from pydantic import BaseModel
from pydantic.color import Color
from models import FileInfoModel
from typing import Optional
from fastapi import Form, File, UploadFile

class SpaceCreateSchema(BaseModel):
  name: str
  color: Color
  icon: FileInfoModel
  
class SpaceUpdateSchema(BaseModel):
  name: str
  color: Color
  icon: Optional[FileInfoModel]

class SpaceCreateFormSchema(BaseModel):
  name: str
  color: Color
  icon_file: UploadFile
  
  def __init__(
    self,
    name: str = Form(...),
    color: str = Form(...),
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
  
  def __init__(
    self,
    name: str = Form(...),
    color: str = Form(...),
    icon_file: Optional[UploadFile] = None,
  ):
    return super().__init__(
      name=name,
      color=color,
      icon_file=icon_file
    )


