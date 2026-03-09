from fastapi.responses import JSONResponse
from fastapi import Request


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": f"Internal server error: {str(exc)}",
        },
    )
