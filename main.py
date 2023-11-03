import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from building.router import building_router

load_dotenv()

app = FastAPI( 
  title='UNI Campus - API', 
  version='0.3.1'
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
  allow_headers=["*"]
)

api_router = APIRouter(prefix='/api')


@api_router.get("/", tags=['Root'])
async def root(
) -> dict:
  """Test Endpoint"""
  return { "message": "UNI Campus - API" }

api_router.include_router(building_router)

app.include_router(api_router)


if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=os.environ.get('DOMAIN'),
    port=int(os.environ.get('PORT')),
    log_level="info",
    reload=True
  )