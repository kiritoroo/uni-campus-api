from fastapi import APIRouter, Request, Response, status, Depends, Path, Query
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic.json import pydantic_encoder
from starlette.background import BackgroundTasks
from typing_extensions import Annotated
import json

from core.log import logger
from core.ratelimit import rate_limited
from exceptions import InternalServerException
from dependencies import dp_auth, dp_admin
from models import ClaimsModel
from building.service import BuildingService
import building.constants as cst 
from building.dependencies import dp_building_col, dp_valid_building, dp_handle_building_create, dp_handle_building_update, dp_handle_building_remove, dp_valid_building_populate
from building.models import BuildingModel
from building.schemas import BuildingCreateFormSchema, BuildingCreateSchema, BuildingUpdateFormSchema, BuildingUpdateSchema, BuildingPopulateSchema
from block.dependencies import dp_block_col
from block.service import BlockService


building_router = APIRouter(prefix='/building', tags=['Building'])

@building_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  request: Request,
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)],
  populate: Annotated[bool | None, Query()] = None
):
  res_buildings = None
  
  if populate:
    res_buildings = await BuildingService(building_col).list_buildings_populate()
  else:
    res_buildings = await BuildingService(building_col).list_buildings()
  res_buildings_json = json.dumps(res_buildings, default=pydantic_encoder)

  return Response(
    content=res_buildings_json,
    status_code=status.HTTP_200_OK
  )
  
@building_router.get('/{id}', **cst.GET_ENDPOINT_DEFINITION)
async def get(
  id: Annotated[str, Path],
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)],
  populate: Annotated[bool | None, Query()] = None
):
  res_building = None

  if populate:
    res_building = await BuildingService(building_col).get_building_populate_by_id(id)
  else:
    res_building = await BuildingService(building_col).get_building_by_id(id)
  res_building_json = json.dumps(res_building, default=pydantic_encoder)

  return Response(
    content=res_building_json,
    status_code=status.HTTP_200_OK
  )
  
@building_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
async def post(
  auth: Annotated[bool, Depends(dp_auth)],
  admin: Annotated[bool, Depends(dp_admin)],
  background_tasks: BackgroundTasks,
  form: Annotated[BuildingCreateFormSchema, Depends()],
  building_create_data: Annotated[BuildingCreateSchema, Depends(dp_handle_building_create)],
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)]
):
  res_building = await BuildingService(building_col).create_building(building_create_data)
  res_building_json = json.dumps(res_building, default=pydantic_encoder)

  return Response(
    content=res_building_json,
    status_code=status.HTTP_201_CREATED,
    background=background_tasks
  )

@building_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: Annotated[str, Path],
  auth: Annotated[bool, Depends(dp_auth)],
  admin: Annotated[bool, Depends(dp_admin)],
  background_tasks: BackgroundTasks,
  building_draft: Annotated[BuildingModel, Depends(dp_valid_building)],
  form: Annotated[BuildingUpdateFormSchema, Depends()],
  building_update_data: Annotated[BuildingUpdateSchema, Depends(dp_handle_building_update)],
  building_col: AsyncIOMotorCollection = Depends(dp_building_col)
):
  res_building = await BuildingService(building_col).update_building(building_draft, building_update_data)
  res_building_json = json.dumps(res_building, default=pydantic_encoder)
  
  return Response(
    content=res_building_json,
    status_code=status.HTTP_200_OK,
    background=background_tasks
  )

@building_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: Annotated[str, Path],
  auth: Annotated[bool, Depends(dp_auth)],
  admin: Annotated[bool, Depends(dp_admin)],
  background_tasks: BackgroundTasks,
  building_draft: Annotated[BuildingPopulateSchema, Depends(dp_valid_building_populate)],
  deleted: Annotated[bool, Depends(dp_handle_building_remove)],
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)],
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)]
):
  success = await BuildingService(building_col).delete_building(building_draft.id)
  success = await BlockService(block_col).delete_blocks_by_building_id(building_draft.id)

  if not success:
    raise InternalServerException()

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
    background=background_tasks
  )
