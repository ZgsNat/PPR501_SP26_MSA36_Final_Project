from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from src.domain.exceptions.base import DomainException
from src.infrastructure.xml.xml_renderer import XMLResponse
import logging

logger = logging.getLogger("uvicorn.error")

# Map hậu tố exception → HTTP status
EXCEPTION_STATUS_MAP = {
    "NotFoundError": status.HTTP_404_NOT_FOUND,
    "AlreadyExistsError": status.HTTP_409_CONFLICT,
    "InvalidDataError": status.HTTP_400_BAD_REQUEST,
}


def register_exception_handlers(app: FastAPI):

    # ===== Domain Errors =====
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        exc_name = exc.__class__.__name__

        status_code = next(
            (
                code
                for suffix, code in EXCEPTION_STATUS_MAP.items()
                if exc_name.endswith(suffix)
            ),
            status.HTTP_400_BAD_REQUEST,
        )

        return XMLResponse(
            status_code=status_code,
            content={
                "error": exc_name,
                "detail": exc.message,
            },
        )

    # ===== Database Errors =====
    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database Error: {exc}")

        return XMLResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "DatabaseError",
                "detail": "Hệ thống tạm thời không thể kết nối dữ liệu. Vui lòng thử lại sau.",
            },
        )

    # ===== Request Validation (FastAPI / Pydantic) =====
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        error = exc.errors()[0]

        return XMLResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "InputValidationError",
                "detail": f"{error.get('msg')} at {error.get('loc')}",
            },
        )

    # ===== Catch-all =====
    @app.exception_handler(Exception)
    async def universal_exception_handler(request: Request, exc: Exception):
        logger.critical(f"Unhandled Error: {exc}")

        return XMLResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "detail": "Đã có lỗi hệ thống xảy ra.",
            },
        )
