import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
import sys

from user.router import user_router
from building.router import building_router
from space.router import space_router

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
  # allow_origins=[
  #   "http://localhost:9999",
  # ],
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin', "Set-Cookie"],
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

static_folder = "static"
subs_static_folder = ["images", "models"]
if not os.path.exists(static_folder):
  os.makedirs(static_folder)
  print(f"Dir {static_folder} created.")
else:
  print(f"Dir {static_folder} existed.")
  
for subfolder in subs_static_folder:
  subfolder_path = os.path.join(static_folder, subfolder)
  if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)
    print(f"Dir {subfolder_path} created.")
  else:
    print(f"Dir {subfolder_path} existed.")
    

app.mount("/static", StaticFiles(directory="static"), name="static")
    
api_router.include_router(user_router)
api_router.include_router(building_router)
api_router.include_router(space_router)

app.include_router(api_router)

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=os.environ.get('DOMAIN'),
    port=int(os.environ.get('PORT')),
    log_level="info",
    reload=True
  )