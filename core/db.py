import asyncio
import motor.motor_asyncio
import core.log as log
import os

conn_str = os.environ.get('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient()

campus_db = client.get_database("campus-db")

async def get_server_info():
  try:
    await client.admin.command('ping')
    log.logger.info("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception:
    log.logger.error("Unable to connect to the server.")
    
loop = asyncio.get_event_loop()
loop.run_until_complete(get_server_info())