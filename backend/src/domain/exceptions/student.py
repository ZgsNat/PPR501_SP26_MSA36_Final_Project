from src.domain.exceptions.base import DomainException

class StudentNotFoundError(DomainException):
    """Lỗi 404: Không tìm thấy"""
    def __init__(self, student_id: str):
        super().__init__(f"Student with ID {student_id} not found")

class StudentAlreadyExistsError(DomainException):
    """Lỗi 409: Đã tồn tại"""
    def __init__(self, student_id: str):
        super().__init__(f"Student with ID {student_id} already exists")

class InvalidStudentDataError(DomainException):
    """Lỗi 400: Dữ liệu không hợp lệ"""
    def __init__(self, message = None):
        super().__init__(f'Invalid Data! {message}')