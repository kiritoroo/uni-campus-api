from pydantic import BaseModel
from logging.config import dictConfig
import logging

LOGGER_NAME: str = "mycoolapp"
LOG_FORMAT: str = "⚡ %(levelprefix)s | %(asctime)s | %(message)s"
LOG_LEVEL: str = "DEBUG"
  
dictConfig({
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "default": {
      "()": "uvicorn.logging.DefaultFormatter",
      "fmt": LOG_FORMAT,
      "datefmt": "%Y-%m-%d %H:%M:%S",
    },
  },
  "handlers": {
    "default": {
      "formatter": "default",
      "class": "logging.StreamHandler",
      "stream": "ext://sys.stderr",
    },
  },
  "loggers": {
    LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
  }
})

logger = logging.getLogger("mycoolapp")