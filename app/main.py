from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ExceptionHandler
from typing import cast

from app.api.routes import auth, tasks, health
from app.core.config import settings
from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logging

# Configure logging at startup
setup_logging()

app = FastAPI(title="Task Manager API")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, cast(ExceptionHandler, http_exception_handler))
app.add_exception_handler(RequestValidationError, cast(ExceptionHandler, validation_exception_handler))
app.add_exception_handler(Exception, global_exception_handler)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Hello from task-manager-api!"}