from fastapi import APIRouter, FastAPI
from app.config.exceptions.business_rule import BusinessRuleException
from app.config.exceptions.not_found import NotFoundException
from app.config.exceptions.unauthorized import UnauthorizedException
from app.config.handlers.business_rule import business_rule_exception_handler
from app.config.handlers.generic import generic_exception_handler
from app.config.handlers.http import http_exception_handler
from app.config.handlers.not_found import not_found_exception_handler
from app.config.handlers.unauthorized import unauthorized_exception_handler
from app.config.handlers.validation import validation_exception_handler
from app.routes.user import user_router
from app.routes.detection import detection_router
from app.routes.yolo import yolo_router
from app.routes.auth.login import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(detection_router)
api_router.include_router(yolo_router)

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(BusinessRuleException, business_rule_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
