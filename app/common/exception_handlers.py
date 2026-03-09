import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.common.exceptions import BusinessException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BusinessException)
    async def business_exception_handler(_request: Request, exc: BusinessException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            errors.append({"field": field, "message": error["msg"]})
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": "입력값이 올바르지 않습니다.", "errors": errors},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(_request: Request, exc: Exception):
        logger.error("서버 오류 발생", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": "서버 오류가 발생했습니다."},
        )
