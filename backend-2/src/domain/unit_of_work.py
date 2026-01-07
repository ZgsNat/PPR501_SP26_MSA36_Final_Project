from abc import ABC, abstractmethod
from typing import Optional
from src.domain.repositories.student_repository import IStudentRepository

class IUnitOfWork(ABC):
    """
    Interface cho Unit of Work.
    Giúp Use Case quản lý transaction mà không phụ thuộc vào SQLAlchemy.
    """
    students: IStudentRepository  # Khai báo các repo sẽ dùng

    @abstractmethod
    def __enter__(self):
        """Bắt đầu context (transaction)"""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Kết thúc context (commit hoặc rollback)"""
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass