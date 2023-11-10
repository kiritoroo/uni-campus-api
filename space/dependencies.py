from core.db import campus_db
from motor.motor_asyncio import AsyncIOMotorCollection

space_col = campus_db.get_collection("space")

async def dp_space_col() -> AsyncIOMotorCollection:
  yield space_col
  
