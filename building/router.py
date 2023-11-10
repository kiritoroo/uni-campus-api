from fastapi import APIRouter, Response, status, Depends, File, UploadFile, Path
from building.service import BuildingService
import building.constants as cst 
from building.dependencies import dp_building_col, dp_valid_building, dp_handle_building_create, dp_handle_building_update, dp_handle_building_remove
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic.json import pydantic_encoder
from core.log import logger
from building.models import BuildingModel
from building.schemas import BuildingCreateFormSchema, BuildingCreateSchema, BuildingUpdateFormSchema, BuildingUpdateSchema
from exceptions import InternalServerException
from typing_extensions import Annotated
from starlette.background import BackgroundTasks
import json

building_router = APIRouter(prefix='/building', tags=['Building'])

@building_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)]
):
  buildings = await BuildingService(building_col).list_buildings()
  buildings_json = json.dumps(buildings, default=pydantic_encoder)
  logger.debug(buildings_json)

  return Response(
    content=buildings_json,
    status_code=status.HTTP_200_OK
  )
  
@building_router.get('/{id}', **cst.GET_ENDPOINT_DEFINITION)
async def get(
  id: str,
  building: Annotated[BuildingModel, Depends(dp_valid_building)],
):
  building_json = json.dumps(building, default=pydantic_encoder)
  logger.debug(building_json)

  return Response(
    content=building_json,
    status_code=status.HTTP_200_OK
  )
  
@building_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
async def post(
  background_tasks: BackgroundTasks,
  form: Annotated[BuildingCreateFormSchema, Depends()],
  building_create_data: Annotated[BuildingCreateSchema, Depends(dp_handle_building_create)],
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)]
):
  res_building = await BuildingService(building_col).create_building(building_create_data)
  res_building_json = json.dumps(res_building, default=pydantic_encoder)
  logger.debug(res_building_json)

  return Response(
    content=res_building_json,
    status_code=status.HTTP_201_CREATED,
    background=background_tasks
  )

@building_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: str,
  background_tasks: BackgroundTasks,
  building_draft: Annotated[BuildingModel, Depends(dp_valid_building)],
  form: Annotated[BuildingUpdateFormSchema, Depends()],
  building_update_data: Annotated[BuildingUpdateSchema, Depends(dp_handle_building_update)],
  building_col: AsyncIOMotorCollection = Depends(dp_building_col)
):
  res_building = await BuildingService(building_col).update_building(building_draft, building_update_data)
  res_building_json = json.dumps(res_building, default=pydantic_encoder)
  logger.debug(res_building_json)
  
  return Response(
    content=res_building_json,
    status_code=status.HTTP_200_OK,
    background=background_tasks
  )

@building_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: Annotated[str, Path],
  background_tasks: BackgroundTasks,
  building_draft: Annotated[BuildingModel, Depends(dp_valid_building)],
  deleted: Annotated[bool, Depends(dp_handle_building_remove)],
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)]
):
  success = await BuildingService(building_col).delete_building(building_draft.id)

  if not success:
    raise InternalServerException()

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
    background=background_tasks
  )
