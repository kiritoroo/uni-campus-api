from fastapi import Depends, status
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.background import BackgroundTasks
from typing_extensions import Annotated
from typing import List
from motor.motor_asyncio import AsyncIOMotorCollection
import os
import uuid
import json

from core.db import campus_db
from core.log import logger
from models import FileInfoModel
from exceptions import InvalidFormData
from block.models import BlockModel
from block.service import BlockService
from block.schemas import BlockCreateFormSchema, BlockCreateSchema, BlockUpdateFormSchema, BlockUpdateSchema
from building.dependencies import dp_building_col
from building.service import BuildingService
from space.dependencies import dp_space_col
from space.service import SpaceService
from utils import write_file


block_col = campus_db.get_collection("block")

async def dp_block_col() -> AsyncIOMotorCollection:
  yield block_col
  
async def dp_valid_block(
  id: str,
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)]
) -> BlockModel:
  block = await BlockService(block_col).get_block_by_id(id)
  return block

async def dp_handle_block_create(
  background_tasks: BackgroundTasks,
  form: Annotated[BlockCreateFormSchema, Depends()],
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
) -> BlockCreateSchema:
  valid_building = await BuildingService(building_col).get_building_by_id(form.building_id)
  valid_space = await SpaceService(space_col).get_space_by_id(form.space_id)

  try:
    gallery_info: List[FileInfoModel] = []
    for image_file in form.gallery:
      image_file_id = str(uuid.uuid4())
      image_file_extension = os.path.splitext(image_file.filename)[-1]
      image_file_location = f"static/images/{image_file_id}{image_file_extension}"

      background_tasks.add_task(write_file, image_file, image_file_location)

      image_info = FileInfoModel(
        id=image_file_id,
        url=image_file_location,
        filename=f"{image_file_id}{image_file_extension}",
        extension=image_file_extension,
        length=image_file.size,
        content_type=image_file.content_type
      )

      gallery_info.append(image_info)

    schema = BlockCreateSchema(
      name=form.name,
      obj_name=form.obj_name,
      building_id=valid_building.id,
      space_id=valid_space.id,
      uses=form.uses,
      direction_url=form.direction_url,
      coordinate=json.loads(form.coordinate),
      marker_position=json.loads(form.marker_position),
      gallery=gallery_info
    )
    
    return schema
  except Exception as e:
    logger.error(e)
    raise InvalidFormData()
