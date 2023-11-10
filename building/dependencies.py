from core.db import campus_db
from motor.motor_asyncio import AsyncIOMotorCollection
from building.models import BuildingModel
from fastapi import Depends, HTTPException, status
from building.service import BuildingService
from motor.motor_asyncio import AsyncIOMotorCollection
from core.log import logger
from building.schemas import BuildingCreateFormSchema, BuildingCreateSchema, BuildingUpdateFormSchema, BuildingUpdateSchema
from typing_extensions import Annotated
from core.log import logger
from models import FileInfoModel
from starlette.background import BackgroundTasks
from utils import write_file
import json
import os
import uuid

building_col = campus_db.get_collection("building")

async def dp_building_col() -> AsyncIOMotorCollection:
  yield building_col
  
async def dp_valid_building(
  id: str,
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)]
) -> BuildingModel:
  building = await BuildingService(building_col).get_building_by_id(id)
  return building
  
async def dp_handle_building_create(
  background_tasks: BackgroundTasks,
  form: Annotated[BuildingCreateFormSchema, Depends()]
) -> BuildingCreateSchema:
  try:
    model_file_id = str(uuid.uuid4())
    model_file_extension = os.path.splitext(form.model_file.filename)[-1]
    model_file_location = f"static/models/{model_file_id}{model_file_extension}"

    background_tasks.add_task(write_file, form.model_file, model_file_location)
    logger.debug({"info": f"file '{form.model_file.filename}' saved at '{model_file_location}'"})


    preview_file_id = str(uuid.uuid4())
    preview_file_extension = os.path.splitext(form.preview_file.filename)[-1]
    preview_file_location = f"static/images/{preview_file_id}{preview_file_extension}"

    background_tasks.add_task(write_file, form.preview_file, preview_file_location)
    logger.debug({"info": f"file '{form.preview_file.filename}' saved at '{preview_file_location}'"})


    schema = BuildingCreateSchema(
      name=form.name,
      space_id=form.space_id,
      uses=form.uses,
      position=json.loads(form.position),
      rotation=json.loads(form.rotation),
      scale=json.loads(form.scale),
      model_3d=FileInfoModel(
        id=model_file_id,
        url=model_file_location,
        filename=f"{model_file_id}{model_file_extension}",
        extension=model_file_extension,
        length=form.model_file.size,
        content_type=form.model_file.content_type
      ),
      preview_img=FileInfoModel(
        id=preview_file_id,
        url=preview_file_location,
        filename=f"{preview_file_id}{preview_file_extension}",
        extension=preview_file_extension,
        length=form.preview_file.size,
        content_type=form.preview_file.content_type
      )
    )
    
    return schema
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid form data")

async def dp_handle_building_update(
  background_tasks: BackgroundTasks,
  building_draft: Annotated[BuildingModel, Depends(dp_valid_building)],
  form: Annotated[BuildingUpdateFormSchema, Depends()]
) -> BuildingUpdateSchema:
  model_file_id = None
  model_file_extension = None
  model_file_location = None

  preview_file_id = None
  preview_file_extension = None
  preview_file_location = None

  try:
    if form.model_file:
      if building_draft.model_3d:
        background_tasks.add_task(os.remove, building_draft.model_3d.url)

      model_file_id = str(uuid.uuid4())
      model_file_extension = os.path.splitext(form.model_file.filename)[-1]
      model_file_location = f"static/models/{model_file_id}{model_file_extension}"

      background_tasks.add_task(write_file, form.model_file, model_file_location)
      logger.debug({"info": f"file '{form.model_file.filename}' resaved at '{model_file_location}'"})


    if form.preview_file:
      if building_draft.preview_img:
        background_tasks.add_task(os.remove, building_draft.preview_img.url)

      preview_file_id = str(uuid.uuid4())
      preview_file_extension = os.path.splitext(form.preview_file.filename)[-1]
      preview_file_location = f"static/images/{preview_file_id}{preview_file_extension}"

      background_tasks.add_task(write_file, form.preview_file, preview_file_location)
      logger.debug({"info": f"file '{form.preview_file.filename}' resaved at '{preview_file_location}'"})


    schema = BuildingUpdateSchema(
      name=form.name,
      space_id=form.space_id,
      uses=form.uses,
      position=json.loads(form.position),
      rotation=json.loads(form.rotation),
      scale=json.loads(form.scale),
      model_3d=FileInfoModel(
        id=model_file_id,
        url=model_file_location,
        filename=f"{model_file_id}{model_file_extension}",
        extension=model_file_extension,
        length=form.model_file.size,
        content_type=form.model_file.content_type
      ) if form.model_file else None,
      preview_img=FileInfoModel(
        id=preview_file_id,
        url=preview_file_location,
        filename=f"{preview_file_id}{preview_file_extension}",
        extension=preview_file_extension,
        length=form.preview_file.size,
        content_type=form.preview_file.content_type
      ) if form.preview_file else None
    )
    
    return schema
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid form data")

async def dp_handle_building_remove(
  background_tasks: BackgroundTasks,
  building_draft: Annotated[BuildingModel, Depends(dp_valid_building)]
) -> bool:
  try:
    if os.path.exists(building_draft.model_3d.url):
      background_tasks.add_task(os.remove, building_draft.model_3d.url)
      logger.debug({"info": f"file '{building_draft.model_3d.url}' removed"})
    else:
      logger.warning({"info": f"file '{building_draft.model_3d.url}' not found"})

    if os.path.exists(building_draft.preview_img.url):
      background_tasks.add_task(os.remove, building_draft.preview_img.url)
      logger.debug({"info": f"file '{building_draft.preview_img.url}' removed"})
    else:
      logger.warning({"info": f"file '{building_draft.preview_img.url}' not found"})

    return True
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sometime with error")
