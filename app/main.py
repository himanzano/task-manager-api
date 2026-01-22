from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ExceptionHandler
from typing import cast

from app.api.routes import auth, tasks, health
from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logging

# Configure logging at startup
setup_logging()

app = FastAPI(title="Task Manager API")

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