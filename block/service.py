from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorCursor
from bson import ObjectId
from datetime import datetime
from typing import Optional

from block.models import BlockModel
from block.exceptions import BlockNotFound
from block.schemas import BlockPopulateSchema, BlockCreateSchema, BlockUpdateSchema


class BlockService:
  def __init__(self, _block_col: AsyncIOMotorCollection) -> None:
    self.block_col = _block_col

  async def list_blocks(self, building_id: Optional[str] = None) -> list[BlockModel]:
    query = {}
    
    if building_id:
      if not ObjectId.is_valid(building_id):
        raise BlockNotFound()
      query['building_id'] = ObjectId(building_id)

    cur: AsyncIOMotorCursor = self.block_col.find(query)
    blocks_raw = await cur.to_list(length=None)
    blocks = [BlockModel(**doc) for doc in blocks_raw]
    return blocks
  
  async def list_blocks_populate(self, building_id: Optional[str] = None) -> list[BlockPopulateSchema]:
    pipeline = [
      {
        '$lookup': {
          'from': 'space',
          'localField': 'space_id',
          'foreignField': '_id',
          'as': 'space'
        }
      },
      {
        '$unwind': '$space'
      }
    ]
    
    if building_id:
      if not ObjectId.is_valid(building_id):
        raise BlockNotFound()
      pipeline.insert(0, {
        '$match': {
          'building_id': ObjectId(building_id)
        }
      })
    
    blocks_raw = await self.block_col.aggregate(pipeline).to_list(length=None)

    blocks = [BlockPopulateSchema(**doc) for doc in blocks_raw]
    return blocks

  async def get_block_by_id(self, id: str) -> BlockModel:
    if not ObjectId.is_valid(id):
      raise BlockNotFound()

    query = {
      'filter': {
        '_id': ObjectId(id)
      }
    }
    block_raw = await self.block_col.find_one(**query) 

    if not block_raw:
      raise BlockNotFound()

    block = BlockModel(**block_raw)
    return block

  async def get_block_populate_by_id(self, id: str) -> BlockPopulateSchema:
    if not ObjectId.is_valid(id):
      raise BlockNotFound()

    block_raw = await self.block_col.aggregate([
      {
        '$match': {'_id': ObjectId(id)}
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
        '$unwind': '$space'
      }
    ]).to_list(length=None)

    if not block_raw:
      raise BlockNotFound()

    block = BlockPopulateSchema(**block_raw[0])
    return block

  async def create_block(self, data: BlockCreateSchema) -> BlockModel:
    create_data = dict(
        **data.model_dump(exclude_none=True),
        is_publish=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    result = await self.block_col.insert_one(document=create_data)
    block = BlockModel(id=result.inserted_id, **create_data)
    return block

  async def update_block(self, draft: BlockModel, data: BlockUpdateSchema) -> BlockModel:
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
    block_raw = await self.block_col.find_one_and_update(**query)

    block = BlockModel(**block_raw)
    return block

  async def delete_block(self, id: str) -> bool:
    query = {
      'filter': {
          '_id': ObjectId(id)
      }
    }
    result = await self.block_col.delete_one(**query)
    return True if result.deleted_count else False

  async def delete_blocks_by_building_id(self, building_id: str) -> bool:
    query = {
        'filter': {
            'building_id': ObjectId(building_id)
        }
    }
    result = await self.block_col.delete_many(**query)
    return True if result.deleted_count else False