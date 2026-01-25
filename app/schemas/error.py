from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    message: str
    details: Optional[Any] = None

    model_config = ConfigDict(extra="forbid")
