from fastapi import APIRouter
import space.constants as cst
space_router = APIRouter(prefix='/space', tags=['Space'])

@space_router.get('/', **cst.GETS_ENDPOINT_DEFINITION)
async def gets(
  
):
  pass

@space_router.get('/{id}', **cst.GET_ENDPOINT_DEFINITION)
async def get(
  id: str
):
  pass

@space_router.post('/', **cst.POST_ENDPOINT_DEFINITION)
async def post(
  
):
  pass

@space_router.put('/{id}', **cst.PUT_ENDPOINT_DEFINITION)
async def put(
  id: str
):
  pass

@space_router.delete('/{id}', **cst.DELETE_ENDPOINT_DEFINITION)
async def delete(
  id: str
):
  pass