from fastapi import APIRouter, Response, status, Depends, Path
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic.json import pydantic_encoder
from typing_extensions import Annotated
from starlette.background import BackgroundTasks
import json

from core.log import logger
from dependencies import dp_auth
from exceptions import InternalServerException
from block.service import BlockService
import block.constants as cst
from block.dependencies import dp_block_col, dp_valid_block, dp_handle_block_create
from block.models import BlockModel
from block.schemas import BlockCreateFormSchema, BlockCreateSchema, BlockUpdateFormSchema, BlockUpdateSchema
from building.dependencies import dp_building_col
from space.dependencies import dp_space_col


block_router = APIRouter(prefix='/block', tags=['Block'])

@block_router.get('/')
async def gets(
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)],
  populate: bool | None = None
):
  res_blocks = None
  
  if populate:
    res_blocks = await BlockService(block_col).list_blocks_populate()
  else:
    res_blocks = await BlockService(block_col).list_blocks()
  res_blocks_json = json.dumps(res_blocks, default=pydantic_encoder)
  logger.debug(res_blocks_json)

  return Response(
    content=res_blocks_json,
    status_code=status.HTTP_200_OK
  )

@block_router.get('/{id}')
async def get(
  id: str,
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)],
  populate: bool | None = None
):
  res_block = None
  if populate:
    res_block = await BlockService(block_col).get_block_populate_by_id(id)
  else:
    res_block = await BlockService(block_col).get_block_by_id(id)
  res_block_json = json.dumps(res_block, default=pydantic_encoder)
  logger.debug(res_block_json)
  
  return Response(
    content=res_block_json,
    status_code=status.HTTP_200_OK
  )

@block_router.post('/')
async def post(
  auth: Annotated[bool, Depends(dp_auth)],
  background_tasks: BackgroundTasks,
  form: Annotated[BlockCreateFormSchema, Depends()],
  building_col: Annotated[AsyncIOMotorCollection, Depends(dp_building_col)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)],
  block_create_data: Annotated[BlockCreateSchema, Depends(dp_handle_block_create)],
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)]
):
  res_block = await BlockService(block_col).create_block(block_create_data)
  res_block_json = json.dumps(res_block, default=pydantic_encoder)
  logger.debug(res_block_json)

  return Response(
    content=res_block_json,
    status_code=status.HTTP_201_CREATED,
    background=background_tasks
  )

@block_router.put('/{id}')
async def put(
  
):
  pass

@block_router.delete('/{id}')
async def delete(
  
):
  pass
