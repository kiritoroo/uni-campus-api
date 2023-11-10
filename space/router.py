from fastapi import APIRouter

space_router = APIRouter(prefix='/space', tags=['Space'])

@space_router.get('/', )
async def gets(
  
):
  pass

@space_router.get('/{id}', )
async def get(
  id: str
):
  pass

@space_router.post('/', )
async def post(
  
):
  pass

@space_router.put('/{id}', )
async def put(
  id: str
):
  pass

@space_router.delete('/{id}')
async def delete(
  id: str
):
  pass