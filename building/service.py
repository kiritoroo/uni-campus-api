from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorCursor
from building.models import BuildingModel
from building.exceptions import BuildingNotFound
from building.schemas import BuildingCreateSchema, BuildingUpdateSchema
from bson import ObjectId
from datetime import datetime

class BuildingService:
  def __init__(self, _building_col: AsyncIOMotorCollection):
    self.building_col = _building_col
  
  async def list_buildings(self) -> list[BuildingModel]:
    cur: AsyncIOMotorCursor = self.building_col.find()
    buildings_raw = await cur.to_list(length=None)
    buildings = [BuildingModel(**doc) for doc in buildings_raw]
    return buildings
  
  async def get_building_by_id(self, id: str) -> BuildingModel | None:
    if not ObjectId.is_valid(id):
      raise BuildingNotFound()

    query = {
      'filter': {
        '_id': ObjectId(id)
      }
    }
    building_raw = await self.building_col.find_one(**query) 

    if not building_raw:
      raise BuildingNotFound()

    building = BuildingModel(**building_raw)
    return building
  
  async def create_building(self, data: BuildingCreateSchema) -> BuildingModel:
    create_data = dict(
      **data.model_dump(exclude_none=True),
      created_at=datetime.utcnow(),
      updated_at=datetime.utcnow()
    )
    result = await self.building_col.insert_one(document=create_data)
    building = BuildingModel(id=result.inserted_id, **create_data)
    return building

  async def update_building(self, id: str, data: BuildingUpdateSchema) -> BuildingModel:
    await self.get_building_by_id(id)

    update_data = dict(
      **data.model_dump(exclude_none=True),
      updated_at=datetime.utcnow()
    )
    
    query = {
      'filter': {
        '_id': ObjectId(id)
      },
      'update': {
        '$set': update_data
      },
      'return_document': True
    }
    building_raw = await self.building_col.find_one_and_update(**query)

    building = BuildingModel(**building_raw)
    return building

  async def delete_building(self, id: str) -> bool:
    await self.get_building_by_id(id)
    
    query = {
      'filter': {
        '_id': ObjectId(id)
      }
    }
    result = await self.building_col.delete_one(**query)
    return True if result.deleted_count else False

