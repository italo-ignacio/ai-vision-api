from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    message = first_error["msg"]

    return JSONResponse(
        status_code=400,
        content={
            "error": "Field validation error",
            "detail": f"Error in field '{field}': {message}",
        },
    )
