from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Internal server error",
            "detail": exc.detail,
        },
    )
