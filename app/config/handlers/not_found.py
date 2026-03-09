from fastapi import Request
from fastapi.responses import JSONResponse
from app.config.exceptions.not_found import NotFoundException


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404, content={"error": "Not Found", "detail": str(exc)}
    )
