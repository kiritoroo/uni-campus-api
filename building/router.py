from fastapi import APIRouter, Response, status, Depends
from building.service import BuildingService
from building.constants import GET_METHOD_DEFINITION
from building.dependencies import dp_building_col
from motor.motor_asyncio import AsyncIOMotorCollection
import json
from pydantic.json import pydantic_encoder

building_router = APIRouter(prefix='/building', tags=['Building'])

@building_router.get('/', **GET_METHOD_DEFINITION)
async def get(
  building_collection: AsyncIOMotorCollection = Depends(dp_building_col)
):
  buildings = await BuildingService(building_collection).list_buildings()
  print(buildings)
  return Response(
    content=json.dumps(buildings, default=pydantic_encoder),
    status_code=status.HTTP_200_OK
  )
  
@building_router.post('/', **GET_METHOD_DEFINITION)
async def post( building_collection: AsyncIOMotorCollection = Depends(dp_building_col)):
  pass

@building_router.put('/', **GET_METHOD_DEFINITION)
async def put( building_collection: AsyncIOMotorCollection = Depends(dp_building_col)):
  pass

@building_router.delete('/', **GET_METHOD_DEFINITION)
async def delete( building_collection: AsyncIOMotorCollection = Depends(dp_building_col)):
  pass
