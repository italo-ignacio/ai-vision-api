from fastapi import Request
from fastapi.responses import JSONResponse
from app.config.exceptions.unauthorized import UnauthorizedException


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=401, content={"error": "Unauthorized", "detail": str(exc)}
    )
