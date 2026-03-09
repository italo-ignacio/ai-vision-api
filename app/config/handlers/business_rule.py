from fastapi import Request
from fastapi.responses import JSONResponse
from app.config.exceptions.business_rule import BusinessRuleException


async def business_rule_exception_handler(request: Request, exc: BusinessRuleException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Business Rule error",
            "detail": str(exc),
        },
    )
