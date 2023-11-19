from fastapi import APIRouter, Response, status, Depends, Path, Query
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
from block.dependencies import dp_block_col, dp_valid_block, dp_handle_block_create, dp_handle_block_update, dp_handle_block_remove
from block.models import BlockModel
from block.schemas import BlockCreateFormSchema, BlockCreateSchema, BlockUpdateFormSchema, BlockUpdateSchema
from building.dependencies import dp_building_col
from space.dependencies import dp_space_col


block_router = APIRouter(prefix='/block', tags=['Block'])

@block_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)],
  populate: Annotated[bool | None, Query()] = None
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

@block_router.get('/{id}', **cst.GET_ENDPOINT_DEFINITION)
async def get(
  id: Annotated[str, Path],
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)],
  populate: Annotated[bool | None, Query()] = None
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

@block_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
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

@block_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: Annotated[str, Path],
  auth: Annotated[bool, Depends(dp_auth)],
  background_tasks: BackgroundTasks,
  block_draft: Annotated[BlockModel, Depends(dp_valid_block)],
  form: Annotated[BlockUpdateFormSchema, Depends()],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)],
  block_update_data: Annotated[BlockUpdateSchema, Depends(dp_handle_block_update)],
  block_col: AsyncIOMotorCollection = Depends(dp_block_col)
):
  res_block = await BlockService(block_col).update_block(block_draft, block_update_data)
  res_block_json = json.dumps(res_block, default=pydantic_encoder)
  logger.debug(res_block_json)
  
  return Response(
    content=res_block_json,
    status_code=status.HTTP_200_OK,
    background=background_tasks
  )

@block_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: Annotated[str, Path],
  auth: Annotated[bool, Depends(dp_auth)],
  background_tasks: BackgroundTasks,
  block_draft: Annotated[BlockModel, Depends(dp_valid_block)],
  deleted: Annotated[bool, Depends(dp_handle_block_remove)],
  block_col: AsyncIOMotorCollection = Depends(dp_block_col)
):
  success = await BlockService(block_col).delete_block(block_draft.id)
  
  if not success:
    raise InternalServerException()
  
  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
    background=background_tasks
  )
