from fastapi import Form, File, UploadFile
from pydantic import BaseModel
from pydantic.color import Color
from typing import Optional

from models import FileInfoModel


class SpaceCreateSchema(BaseModel):
  name: str
  color: str
  icon: FileInfoModel
  order: int
  
class SpaceUpdateSchema(BaseModel):
  name: Optional[str]
  color: Optional[str]
  icon: Optional[FileInfoModel]
  order: Optional[int]
  is_publish: Optional[bool]

class SpaceCreateFormSchema(BaseModel):
  name: str
  color: Color
  icon_file: UploadFile
  order: int
  
  def __init__(
    self,
    name: str = Form(...),
    color: Color = Form(...),
    icon_file: UploadFile = File(),
    order: int = Form(...)
  ):
    return super().__init__(
      name=name,
      color=color,
      icon_file=icon_file,
      order=order
    )

class SpaceUpdateFormSchema(BaseModel):
  name: Optional[str]
  color: Optional[Color]
  icon_file: Optional[UploadFile]
  order: Optional[int]
  is_publish: Optional[bool]
  
  def __init__(
    self,
    name: str = Form(None),
    color: Color = Form(None),
    icon_file: UploadFile = None,
    order: int = Form(None),
    is_publish: bool = Form(None)
  ):
    return super().__init__(
      name=name,
      color=color,
      icon_file=icon_file,
      order=order,
      is_publish=is_publish
    )
