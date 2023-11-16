from fastapi import APIRouter, Response, status, Depends, Path
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic.json import pydantic_encoder
from exceptions import InternalServerException
from typing_extensions import Annotated
from starlette.background import BackgroundTasks
from dependencies import dp_auth
from core.log import logger
import json

block_router = APIRouter(prefix='/space')