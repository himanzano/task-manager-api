from typing import Any, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    details: Optional[Any] = None
