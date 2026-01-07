from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from src.domain.exceptions.base import DomainException
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from src.infrastructure.xml.xml_renderer import XMLResponse # Đảm bảo trả về XML
import logging

# Map đuôi của tên lỗi sang HTTP Status Code
EXCEPTION_STATUS_MAP = {
    "NotFoundError": status.HTTP_404_NOT_FOUND,       # Ví dụ: StudentNotFoundError -> 404
    "AlreadyExistsError": status.HTTP_409_CONFLICT,   # Ví dụ: StudentAlreadyExistsError -> 409
    "InvalidDataError": status.HTTP_400_BAD_REQUEST,  # Ví dụ: InvalidStudentDataError -> 400
    "Error": status.HTTP_400_BAD_REQUEST              # Mặc định các lỗi Domain khác -> 400
}
logger = logging.getLogger("uvicorn.error")

def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        # Lấy tên class lỗi (vd: StudentNotFoundError)
        exc_name = exc.__class__.__name__
        
        # Tìm status code dựa trên đuôi tên lỗi
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        for suffix, code in EXCEPTION_STATUS_MAP.items():
            if exc_name.endswith(suffix):
                status_code = code
                break
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": exc_name,
                "detail": exc.message
            }
        )
    # 1. Bắt các lỗi cụ thể của Database (SQLAlchemy)
    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database Error: {str(exc)}") # Log lại lỗi chi tiết cho Dev
        
        return XMLResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "DatabaseError",
                "detail": "Hệ thống tạm thời không thể kết nối dữ liệu. Vui lòng thử lại sau."
            }
        )

    # 2. Bắt TẤT CẢ các lỗi còn lại (Lỗi code, lỗi logic lạ...)
    # Đây là cái lưới cuối cùng để đảm bảo server không bao giờ "nổ" trả về HTML
    @app.exception_handler(Exception)
    async def universal_exception_handler(request: Request, exc: Exception):
        logger.critical(f"Unhandled Error: {str(exc)}")
        
        return XMLResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "detail": "Đã có lỗi hệ thống xảy ra. Đội ngũ kỹ thuật đã được thông báo."
            }
        )

    