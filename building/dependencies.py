from core.db import campus_db
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection
from building.models import BuildingModel
from fastapi import Depends, HTTPException, status
from building.service import BuildingService
from motor.motor_asyncio import AsyncIOMotorCollection
from core.log import logger
from building.schemas import BuildingCreateFormSchema, BuildingCreateSchema
from typing_extensions import Annotated
import json
import aiofiles
import os
from datetime import datetime
import uuid
from core.log import logger

building_col = campus_db.get_collection("building")

async def dp_building_col() -> AsyncIOMotorCollection:
  yield building_col
  
async def dp_valid_building(id: str, building_col: AsyncIOMotorCollection = Depends(dp_building_col)) -> BuildingModel:
  building = await BuildingService(building_col).get_building_by_id(id)
  return building
  
async def dp_handle_building_create_form(form: Annotated[BuildingCreateFormSchema, Depends()]) -> BuildingCreateSchema:
  current_datetime = datetime.now()

  try:
    model_file_id = str(uuid.uuid4())
    model_filename = os.path.splitext(form.model_file.filename)[0]
    model_file_extension = os.path.splitext(form.model_file.filename)[-1]
    model_file_location = f"static/models/{model_file_id}{model_file_extension}"

    with open(model_file_location, "wb+") as file_object:
      file_object.write(form.model_file.file.read())
    logger.debug({"info": f"file '{form.model_file.filename}' saved at '{model_file_location}'"})


    preview_file_id = str(uuid.uuid4())
    preview_filename = os.path.splitext(form.preview_file.filename)[0]
    preview_file_extension = os.path.splitext(form.preview_file.filename)[-1]
    preview_file_location = f"static/images/{preview_file_id}{preview_file_extension}"

    with open(preview_file_location, "wb+") as file_object:
      file_object.write(form.preview_file.file.read())
    logger.debug({"info": f"file '{form.preview_file.filename}' saved at '{preview_file_location}'"})


    schema = BuildingCreateSchema(
      name=form.name,
      space_id=form.space_id,
      uses=form.uses,
      position=json.loads(form.position),
      rotation=json.loads(form.rotation),
      scale=json.loads(form.scale),
      model_url=f"/{model_file_location}",
      preview_url=f"/{preview_file_location}"
    )
    
    return schema
  except json.JSONDecodeError as e:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid form data")
