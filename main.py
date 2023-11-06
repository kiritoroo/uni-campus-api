import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import asyncio
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.background import BackgroundTask
import psutil
import signal
import sys
from fastapi.staticfiles import StaticFiles

from building.router import building_router

load_dotenv()

app = FastAPI( 
  title='UNI Campus - API', 
  version='0.3.1'
)

# async def exit_app():
#   loop = asyncio.get_running_loop()
#   loop.stop()
  
    
def receive_signal(signalNumber, frame):
    print('Received:', signalNumber)
    sys.exit()
  
@app.on_event("startup")
async def startup_event():
    import signal
    signal.signal(signal.SIGINT, receive_signal)

# @app.on_event('shutdown')
# def shutdown_event():
#     print('Shutting down...!')
    
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     task = BackgroundTask(exit_app)
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code, background=task)

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
  return { "message": "UNI Campus - APIasdf" }

# @app.get("/quit")
# def iquit():
#     parent_pid = os.getpid()
#     parent = psutil.Process(parent_pid)
#     for child in parent.children(recursive=True):
#         child.kill()
#     parent.kill()

app.mount("/static", StaticFiles(directory="static"), name="static")
    
api_router.include_router(building_router)

app.include_router(api_router)

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=os.environ.get('DOMAIN'),
    port=int(os.environ.get('PORT')),
    log_level="info",
    reload=False
  )