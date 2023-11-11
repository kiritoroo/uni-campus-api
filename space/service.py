from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorCursor
from space.models import SpaceModel
from space.exceptions import SpaceNotFound
from space.schemas import SpaceCreateSchema, SpaceUpdateSchema
from bson import ObjectId
from datetime import datetime

class SpaceService:
  def __init__(self, _space_col: AsyncIOMotorCollection):
    self.space_col = _space_col
    
  async def list_space(self) -> list[SpaceModel]:
    cur: AsyncIOMotorCursor = self.space_col.find()
    spaces_raw = await cur.to_list(length=None)
    spaces = [SpaceModel(**doc) for doc in spaces_raw]
    return spaces
  
  async def get_space_by_id(self, id: str) -> SpaceModel:
    if not ObjectId.is_valid(id):
      raise SpaceNotFound()

    query = {
      'filter': {
        '_id': ObjectId(id)
      }
    }
    space_raw = await self.space_col.find_one(**query)

    if not space_raw:
      raise SpaceNotFound()

    space = SpaceModel(**space_raw)
    return space
  
  async def create_space(self, data: SpaceCreateSchema) -> SpaceModel:
    create_data = dict(
      **data.model_dump(exclude_none=True),
      created_at=datetime.utcnow(),
      updated_at=datetime.utcnow()
    )
    result = await self.space_col.insert_one(document=create_data)
    space = SpaceModel(id=result.inserted_id, **create_data)
    return space
  
  async def update_space(self, draft: SpaceModel, data: SpaceUpdateSchema) -> SpaceModel:
    update_data = dict(
      **data.model_dump(exclude_none=True),
      **{k: v for k, v in draft.model_dump(exclude_none=True, exclude=['id', 'updated_at']).items() if k not in data.model_dump()},
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
    space_raw = await self.space_col.find_one_and_update(**query)

    space = SpaceModel(**space_raw)
    return space

  async def delete_space(self, id: str) -> bool:
    query = {
      'filter': {
          '_id': ObjectId(id)
      }
    }
    result = await self.space_col.delete_one(**query)
    return True if result.deleted_count else False