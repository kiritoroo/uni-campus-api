from fastapi import APIRouter, Response, status, Depends
from building.service import BuildingService
import building.constants as cst 
from building.dependencies import dp_building_col, dp_valid_building
from motor.motor_asyncio import AsyncIOMotorCollection
import json
from pydantic.json import pydantic_encoder
from core.log import logger
from building.models import BuildingModel
from building.schemas import BuildingCreateSchema, BuildingUpdateSchema
from exceptions import InternalServerException

building_router = APIRouter(prefix='/building', tags=['Building'])

@building_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  building_col: AsyncIOMotorCollection = Depends(dp_building_col)
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
  building: BuildingModel | None = Depends(dp_valid_building),
):
  building_json = json.dumps(building, default=pydantic_encoder)
  logger.debug(building_json)

  return Response(
    content=building_json,
    status_code=status.HTTP_200_OK
  )
  
@building_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
async def post(
  body: BuildingCreateSchema,
  building_col: AsyncIOMotorCollection = Depends(dp_building_col)
):
  building = await BuildingService(building_col).create_building(body)
  building_json = json.dumps(building, default=pydantic_encoder)
  logger.debug(building_json)

  return Response(
    content=building_json,
    status_code=status.HTTP_201_CREATED
  )

@building_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: str,
  body: BuildingUpdateSchema,
  building_col: AsyncIOMotorCollection = Depends(dp_building_col)
):
  building = await BuildingService(building_col).update_building(id, body)
  building_json = json.dumps(building, default=pydantic_encoder)
  logger.debug(building_json)
  
  return Response(
    content=building_json,
    status_code=status.HTTP_200_OK
  )

@building_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: str,
  building_col: AsyncIOMotorCollection = Depends(dp_building_col)
):
  success = await BuildingService(building_col).delete_building(id)

  if not success:
    raise InternalServerException()

  return Response(
    status_code=status.HTTP_204_NO_CONTENT
  )
