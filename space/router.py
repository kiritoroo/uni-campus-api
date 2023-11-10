from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
import space.constants as cst
from space.dependencies import dp_space_col
from typing_extensions import Annotated

space_router = APIRouter(prefix='/space', tags=['Space'])

@space_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  pass

@space_router.get('/{id}', **cst.GET_ENDPOINT_DEFINITION)
async def get(
  id: str,
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  pass

@space_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
async def post(
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  pass

@space_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: str,
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  pass

@space_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: str,
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  pass