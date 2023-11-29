from fastapi import Depends, status
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.background import BackgroundTasks
from typing_extensions import Annotated
from motor.motor_asyncio import AsyncIOMotorCollection
import os
import uuid

from core.db import campus_db
from core.log import logger
from exceptions import InternalServerException, InvalidFormData
from models import FileInfoModel
from space.schemas import SpaceCreateFormSchema, SpaceCreateSchema, SpaceUpdateFormSchema, SpaceUpdateSchema
from space.models import SpaceModel
from space.service import SpaceService
from utils import write_file


space_col = campus_db.get_collection("space")

async def dp_space_col() -> AsyncIOMotorCollection:
  yield space_col
  
async def dp_valid_space(
  id: str,
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
) -> SpaceModel:
  space = await SpaceService(space_col).get_space_by_id(id)
  return space
  
async def dp_handle_space_create(
  background_tasks: BackgroundTasks,
  form: Annotated[SpaceCreateFormSchema, Depends()]
) -> SpaceCreateSchema:
  try:
    icon_file_id = str(uuid.uuid4())
    icon_file_extension = os.path.splitext(form.icon_file.filename)[-1]
    icon_file_location = f"static/images/{icon_file_id}{icon_file_extension}"

    background_tasks.add_task(write_file, form.icon_file, icon_file_location)
    logger.debug({"info": f"file '{form.icon_file.filename}' saved at '{icon_file_location}'"})

    schema = SpaceCreateSchema(
      name=form.name,
      color=form.color.as_hex(),
      icon=FileInfoModel(
        id=icon_file_id,
        url=icon_file_location,
        filename=f"{icon_file_id}{icon_file_extension}",
        extension=icon_file_extension,
        length=form.icon_file.size,
        content_type=form.icon_file.content_type
      )
    )

    return schema
  except Exception as e:
    logger.error(e)
    raise InvalidFormData()

async def dp_handle_space_update(
  background_tasks: BackgroundTasks,
  space_draft: Annotated[SpaceModel, Depends(dp_valid_space)],
  form: Annotated[SpaceUpdateFormSchema, Depends()]
) -> SpaceUpdateSchema:
  icon_file_id = None
  icon_file_extension = None
  icon_file_location = None

  try:
    if form.icon_file:
      if space_draft.icon:
        background_tasks.add_task(os.remove, space_draft.icon.url)
      icon_file_id = str(uuid.uuid4())
      icon_file_extension = os.path.splitext(form.icon_file.filename)[-1]
      icon_file_location = f"static/images/{icon_file_id}{icon_file_extension}"
    
      background_tasks.add_task(write_file, form.icon_file, icon_file_location)
      logger.debug({"info": f"file '{form.icon_file.filename}' saved at '{icon_file_location}'"})

    schema = SpaceUpdateSchema(
      name=form.name,
      color=form.color.as_hex() if form.color else None,
      icon=FileInfoModel(
        id=icon_file_id,
        url=icon_file_location,
        filename=f"{icon_file_id}{icon_file_location}",
        extension=icon_file_location,
        length=form.icon_file.size,
        content_type=form.icon_file.content_type
      ) if form.icon_file else None,
      is_publish=form.is_publish
    )
    logger.info(schema)
    return schema
  except Exception as e:
    logger.error(e)
    raise InvalidFormData()

async def dp_handle_space_remove(
  background_tasks: BackgroundTasks,
  space_draft: Annotated[SpaceModel, Depends(dp_valid_space)],
) -> bool:
  try:
    if os.path.exists(space_draft.icon.url):
      background_tasks.add_task(os.remove, space_draft.icon.url)
      logger.debug({"info": f"file '{space_draft.icon.url}' removed"})
    else:
      logger.warning({"info": f"file '{space_draft.icon.url}' not found"})

    return True
  except Exception as e:
    logger.error(e)
    raise InternalServerException()
