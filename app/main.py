import logging
import sys
from fastapi import FastAPI

from app.log.logging_lib import RouterLoggingMiddleware
from app.api_v1.endpoints.routers import router as authorization_routes
from app.core.config import logging_config

logging.config.dictConfig(logging_config)

app = FastAPI()
app.add_middleware(RouterLoggingMiddleware,
                   logger=logging.getLogger("elastic-logger"))
app.include_router(router=authorization_routes, prefix="")
