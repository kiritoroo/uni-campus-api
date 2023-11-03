from core.db import campus_db
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection

building_col = campus_db.get_collection("building")

async def dp_building_col() -> AsyncIOMotorCollection:
  yield building_col