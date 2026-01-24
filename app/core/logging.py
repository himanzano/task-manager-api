import logging
import sys

from fastapi import Request


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    # Suppress verbose logs from third-party libraries if needed
    # logging.getLogger("multipart").setLevel(logging.WARNING)


async def log_request_middleware(request: Request, call_next):
    # Simple request logging
    # In production, this might be handled by uvicorn's access log or a reverse proxy.
    # We add this for application-level visibility if needed, but uvicorn already logs access.
    # So we focus on ensuring the global config is set.

    response = await call_next(request)
    return response
