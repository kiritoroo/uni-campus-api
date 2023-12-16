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
  slug: str
  
class SpaceUpdateSchema(BaseModel):
  name: Optional[str]
  color: Optional[str]
  icon: Optional[FileInfoModel]
  order: Optional[int]
  slug: Optional[str]
  is_publish: Optional[bool]

class SpaceCreateFormSchema(BaseModel):
  name: str
  color: Color
  icon_file: UploadFile
  order: int
  slug: str
  
  def __init__(
    self,
    name: str = Form(...),
    color: Color = Form(...),
    icon_file: UploadFile = File(),
    order: int = Form(...),
    slug: str = Form(...),
  ):
    return super().__init__(
      name=name,
      color=color,
      icon_file=icon_file,
      order=order,
      slug= slug
    )

class SpaceUpdateFormSchema(BaseModel):
  name: Optional[str]
  color: Optional[Color]
  icon_file: Optional[UploadFile]
  order: Optional[int]
  slug: Optional[str]
  is_publish: Optional[bool]
  
  def __init__(
    self,
    name: str = Form(None),
    color: Color = Form(None),
    icon_file: UploadFile = None,
    order: int = Form(None),
    slug: str = Form(None),
    is_publish: bool = Form(None),
  ):
    return super().__init__(
      name=name,
      color=color,
      icon_file=icon_file,
      order=order,
      slug=slug,
      is_publish=is_publish
    )
