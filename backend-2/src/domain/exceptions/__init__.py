"""Domain exceptions package."""
from src.domain.exceptions.base import DomainException
from src.domain.exceptions.student import (
    StudentNotFoundError,
    StudentAlreadyExistsError,
    InvalidStudentDataError,
)

__all__ = [
    "DomainException",
    "StudentNotFoundError",
    "StudentAlreadyExistsError",
    "InvalidStudentDataError",
]