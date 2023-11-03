from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorCursor
from building.models import BuildingModel
from building.exceptions import BuildingNotFound
from bson import ObjectId

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