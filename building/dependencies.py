from core.db import campus_db
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection
from building.models import BuildingModel
from fastapi import Depends
from building.service import BuildingService
from motor.motor_asyncio import AsyncIOMotorCollection
from core.log import logger

building_col = campus_db.get_collection("building")

async def dp_building_col() -> AsyncIOMotorCollection:
  yield building_col
  
async def dp_valid_building(id: str, building_col: AsyncIOMotorCollection = Depends(dp_building_col)) -> BuildingModel:
  building = await BuildingService(building_col).get_building_by_id(id)
  return building
  