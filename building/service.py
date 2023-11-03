from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorCursor
from building.models import BuildingModel

class BuildingService:
  def __init__(self, _building_col: AsyncIOMotorCollection):
    self.building_col = _building_col
  
  async def list_buildings(self) -> list[BuildingModel]:
    cur: AsyncIOMotorCursor = self.building_col.find()
    buildings_list = await cur.to_list(length=None)
    buildings = [BuildingModel(**doc) for doc in buildings_list]
    return buildings