from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.domain.entities.student import Student, StudentFilter
from src.shared.pagination import PaginationParams, PagedResult

class IStudentRepository(ABC):
    @abstractmethod
    def get_list(self, filters: StudentFilter, pagination: PaginationParams) -> PagedResult[Student]:
        pass

    @abstractmethod
    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        pass

    @abstractmethod
    def create(self, student: Student) -> Student:
        pass

    @abstractmethod
    def update(self, student_id: str, updates: Dict[str, Any]) -> Optional[Student]:
        pass

    @abstractmethod
    def delete(self, student_id: str) -> bool:
        pass