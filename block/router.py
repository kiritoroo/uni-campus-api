from fastapi import APIRouter, Response, status, Depends, Path
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic.json import pydantic_encoder
from exceptions import InternalServerException
from typing_extensions import Annotated
from starlette.background import BackgroundTasks
from dependencies import dp_auth
from core.log import logger
import json

block_router = APIRouter(prefix='/block', tags=['Block'])

@block_router.get('/')
async def gets(
  
):
  pass

@block_router.get('/{id}')
async def get(
  
):
  pass

@block_router.post('/')
async def post(
  
):
  pass

@block_router.put('/{id}')
async def put(
  
):
  pass

@block_router.delete('/{id}')
async def delete(
  
):
  pass
