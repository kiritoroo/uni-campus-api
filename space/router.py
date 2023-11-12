from fastapi import APIRouter, Depends, Response, status
from space.service import SpaceService
from motor.motor_asyncio import AsyncIOMotorCollection
import space.constants as cst
from space.dependencies import dp_space_col, dp_valid_space, dp_handle_space_create, dp_handle_space_update, dp_handle_space_remove
from typing_extensions import Annotated
from starlette.background import BackgroundTasks
from space.schemas import SpaceCreateFormSchema, SpaceCreateSchema, SpaceUpdateFormSchema, SpaceUpdateSchema
from exceptions import InternalServerException
from space.models import SpaceModel
from pydantic.json import pydantic_encoder
from core.log import logger
from dependencies import dp_auth
import json

space_router = APIRouter(prefix='/space', tags=['Space'])

@space_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  res_spaces = await SpaceService(space_col).list_space()
  res_spaces_json = json.dumps(res_spaces, default=pydantic_encoder)
  logger.debug(res_spaces_json)

  return Response(
    content=res_spaces_json,
    status_code=status.HTTP_200_OK
  )

@space_router.get('/{id}', **cst.GET_ENDPOINT_DEFINITION)
async def get(
  id: str,
  space: Annotated[SpaceModel, Depends(dp_valid_space)]
):
  space_json = json.dumps(space, default=pydantic_encoder)
  logger.debug(space_json)

  return Response(
    content=space_json,
    status_code=status.HTTP_200_OK
  )

@space_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
async def post(
  auth: Annotated[bool, Depends(dp_auth)],
  background_tasks: BackgroundTasks,
  form: Annotated[SpaceCreateFormSchema, Depends()],
  space_create_data: Annotated[SpaceCreateSchema, Depends(dp_handle_space_create)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  res_space = await SpaceService(space_col).create_space(space_create_data)
  res_space_json = json.dumps(res_space, default=pydantic_encoder)
  logger.debug(res_space_json)
  
  return Response(
    content=res_space_json,
    status_code=status.HTTP_201_CREATED,
    background=background_tasks
  )

@space_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: str,
  auth: Annotated[bool, Depends(dp_auth)],
  background_tasks: BackgroundTasks,
  space_draft: Annotated[SpaceModel, Depends(dp_valid_space)],
  form: Annotated[SpaceUpdateFormSchema, Depends()],
  space_update_data: Annotated[SpaceUpdateSchema, Depends(dp_handle_space_update)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  res_space = await SpaceService(space_col).update_space(space_draft, space_update_data)
  res_space_json = json.dumps(res_space, default=pydantic_encoder)
  logger.debug(res_space_json)

  return Response(
    content=res_space_json,
    status_code=status.HTTP_200_OK,
    background=background_tasks
  )

@space_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: str,
  auth: Annotated[bool, Depends(dp_auth)],
  background_tasks: BackgroundTasks,
  space_draft: Annotated[SpaceModel, Depends(dp_valid_space)],
  deleted: Annotated[bool, Depends(dp_handle_space_remove)],
  space_col: Annotated[AsyncIOMotorCollection, Depends(dp_space_col)]
):
  sucess = await SpaceService(space_col).delete_space(space_draft.id)
  
  if not sucess:
    raise InternalServerException()

  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
    background=background_tasks
  )