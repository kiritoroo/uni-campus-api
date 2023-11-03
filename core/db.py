import asyncio
import motor.motor_asyncio
from pymongo.server_api import ServerApi
import core.log as log
import os

conn_str = os.environ.get('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, server_api=ServerApi('1'))

campus_db = client.get_database("campus_db")

async def ping_server():
  try:
    await client.admin.command('ping')
    log.logger.info("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception:
    log.logger.error("Unable to connect to the server.")
  
# asyncio.run(ping_server())