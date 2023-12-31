from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorCursor
from typing import List
from bson import ObjectId
from datetime import datetime

from building.models import BuildingModel
from building.exceptions import BuildingNotFound
from building.schemas import BuildingPopulateSchema, BuildingCreateSchema, BuildingUpdateSchema


class BuildingService:
  def __init__(self, _building_col: AsyncIOMotorCollection):
    self.building_col = _building_col
  
  async def list_buildings(self) -> list[BuildingModel]:
    cur: AsyncIOMotorCursor = self.building_col.find()
    buildings_raw = await cur.to_list(length=None)
    buildings = [BuildingModel(**doc) for doc in buildings_raw]
    return buildings
  
  async def list_buildings_populate(self) -> List[BuildingPopulateSchema]:
    buildings_raw = await self.building_col.aggregate([
      {
        '$lookup': {
          'from': 'block',
          'let': {'building_id': '$_id'},
          'pipeline': [
            {
              '$match': {
                '$expr': {'$eq': ['$building_id', '$$building_id']}
               }
            },
            {
              '$lookup': {
                'from': 'space',
                'localField': 'space_id',
                'foreignField': '_id',
                'as': 'space'
              }
            },
            {
              '$unwind': {
                'path': '$space',
                'preserveNullAndEmptyArrays': True
              }
            }
          ],
          'as': 'blocks'
        }
      },
      {
        '$addFields': {
          'blocks': {
            '$cond': {
              'if': { '$eq': ['$blocks', []] },
              'then': [],
              'else': '$blocks'
            }
          }
        }
      }
    ]).to_list(length=None)
  
    buildings = [BuildingPopulateSchema(**doc) for doc in buildings_raw]
    return buildings
  
  async def get_building_by_id(self, id: str) -> BuildingModel:
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
  
  async def get_building_populate_by_id(self, id: str) -> BuildingPopulateSchema:
    if not ObjectId.is_valid(id):
      raise BuildingNotFound()

    building_raw = await self.building_col.aggregate([
      {
        '$match': {'_id': ObjectId(id)}
      },
      {
        '$lookup': {
          'from': 'block',
          'let': {'building_id': '$_id'},
          'pipeline': [
            {
              '$match': {
                '$expr': {'$eq': ['$building_id', '$$building_id']}
               }
            },
            {
              '$lookup': {
                'from': 'space',
                'localField': 'space_id',
                'foreignField': '_id',
                'as': 'space'
              }
            },
            {
              '$unwind': {
                'path': '$space',
                'preserveNullAndEmptyArrays': True
              }
            }
          ],
          'as': 'blocks'
        }
      },
      {
        '$addFields': {
          'blocks': {
            '$cond': {
              'if': { '$eq': ['$blocks', []] },
              'then': [],
              'else': '$blocks'
            }
          }
        }
      }
    ]).to_list(length=None)

    if not building_raw:
      raise BuildingNotFound()

    block = BuildingPopulateSchema(**building_raw[0])
    return block
  
  async def create_building(self, data: BuildingCreateSchema) -> BuildingModel:
    create_data = dict(
      **data.model_dump(exclude_none=True),
      is_publish=False,
      created_at=datetime.utcnow(),
      updated_at=datetime.utcnow()
    )
    result = await self.building_col.insert_one(document=create_data)
    building = BuildingModel(id=result.inserted_id, **create_data)
    return building

  async def update_building(self, draft: BuildingModel, data: BuildingUpdateSchema) -> BuildingModel:
    update_data = dict(
      **data.model_dump(exclude_none=True),
      **{k: v for k, v in draft.model_dump(exclude_none=True, exclude=['id','updated_at']).items() if k not in data.model_dump()},
      updated_at=datetime.utcnow()
    )
    
    query = {
      'filter': {
        '_id': ObjectId(draft.id)
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
    query = {
      'filter': {
        '_id': ObjectId(id)
      }
    }
    result = await self.building_col.delete_one(**query)
    return True if result.deleted_count else False

