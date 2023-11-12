from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection
from user.models import UserModel
from user.schemas import UserSignupSchema
from bson import ObjectId
from user.exceptions import UserNotFound

class UserService:
  def __init__(self, _user_col: AsyncIOMotorCollection):
    self.user_col = _user_col
    
  async def get_user_by_username(self, username: str) -> UserModel | None:
    query = {
      'filter': {
        'username': username
      }
    }
    
    user_raw = await self.user_col.find_one(**query)
    return UserModel(**user_raw) if user_raw else None
  
  async def get_user_by_id(self, id: str) -> UserModel:
    if not ObjectId.is_valid(id):
      raise UserNotFound()
    
    query = {
      'filter': {
        '_id': ObjectId(id)
      }
    }
    user_raw = await self.user_col.find_one(**query)
    
    if not user_raw:
      raise UserNotFound()
    
    user = UserModel(**user_raw)
    return user
  
  async def create_user(self, data: UserSignupSchema) -> UserModel:
    create_data = dict(
      **data.model_dump(exclude_none=True),
      created_at=datetime.utcnow(),
      updated_at=datetime.utcnow(),
      last_login=None
    )
    result = await self.user_col.insert_one(document=create_data)
    user = UserModel(id=result.inserted_id, **create_data)
    return user