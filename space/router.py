from fastapi import APIRouter, Depends, Response, status, Path
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.background import BackgroundTasks
from typing_extensions import Annotated
from pydantic.json import pydantic_encoder
import json

from core.log import logger
from exceptions import InternalServerException
from dependencies import dp_auth, dp_admin
from models import ClaimsModel
import space.constants as cst
from space.dependencies import dp_space_col, dp_valid_space, dp_handle_space_create, dp_handle_space_update, dp_handle_space_remove
from space.service import SpaceService
from space.schemas import SpaceCreateFormSchema, SpaceCreateSchema, SpaceUpdateFormSchema, SpaceUpdateSchema
from space.models import SpaceModel
from block.service import BlockService
from block.dependencies import dp_block_col


space_router = APIRouter(prefix='/space', tags=['Space'])

@space_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  res_spaces = await SpaceService(space_col).list_space()
  res_spaces_json = json.dumps(res_spaces, default=pydantic_encoder)

  return Response(
    content=res_spaces_json,
    status_code=status.HTTP_200_OK
  )

@space_router.get('/{id}', **cst.GET_ENDPOINT_DEFINITION)
async def get(
  id: Annotated[str, Path],
  space: Annotated[SpaceModel, Depends(dp_valid_space)]
):
  space_json = json.dumps(space, default=pydantic_encoder)

  return Response(
    content=space_json,
    status_code=status.HTTP_200_OK
  )

@space_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
async def post(
  auth: Annotated[ClaimsModel, Depends(dp_auth)],
  admin: Annotated[bool, Depends(dp_admin)],
  background_tasks: BackgroundTasks,
  form: Annotated[SpaceCreateFormSchema, Depends()],
  space_create_data: Annotated[SpaceCreateSchema, Depends(dp_handle_space_create)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  res_space = await SpaceService(space_col).create_space(space_create_data)
  res_space_json = json.dumps(res_space, default=pydantic_encoder)
  
  return Response(
    content=res_space_json,
    status_code=status.HTTP_201_CREATED,
    background=background_tasks
  )

@space_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: Annotated[str, Path],
  auth: Annotated[ClaimsModel, Depends(dp_auth)],
  admin: Annotated[bool, Depends(dp_admin)],
  background_tasks: BackgroundTasks,
  space_draft: Annotated[SpaceModel, Depends(dp_valid_space)],
  form: Annotated[SpaceUpdateFormSchema, Depends()],
  space_update_data: Annotated[SpaceUpdateSchema, Depends(dp_handle_space_update)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  res_space = await SpaceService(space_col).update_space(space_draft, space_update_data)
  res_space_json = json.dumps(res_space, default=pydantic_encoder)

  return Response(
    content=res_space_json,
    status_code=status.HTTP_200_OK,
    background=background_tasks
  )

@space_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: Annotated[str, Path],
  auth: Annotated[ClaimsModel, Depends(dp_auth)],
  admin: Annotated[bool, Depends(dp_admin)],
  background_tasks: BackgroundTasks,
  space_draft: Annotated[SpaceModel, Depends(dp_valid_space)],
  deleted: Annotated[bool, Depends(dp_handle_space_remove)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)],
  block_col: Annotated[AsyncIOMotorCollection, Depends(dp_block_col)]
):
  success = await SpaceService(space_col).delete_space(space_draft.id)
  success = await BlockService(block_col).remove_space(space_draft.id)
  
  if not success:
    raise InternalServerException()

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
    background=background_tasks
  )