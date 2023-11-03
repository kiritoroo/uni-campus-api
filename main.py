import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import core.db

load_dotenv()

app = FastAPI( 
  # openapi_url='/docs',
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

@app.get("/", tags=['Root'])
async def root(
) -> dict:
  """Test Endpoint"""
  return { "message": "UNI Campus - API" }

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=os.environ.get('DOMAIN'),
    port=int(os.environ.get('PORT')),
    log_level="info",
    reload=True
  )