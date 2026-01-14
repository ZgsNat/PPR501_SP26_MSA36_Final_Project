# domain/repositories/student_reader.py
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.student import Student, StudentFilter
from src.shared.pagination import PaginationParams, PagedResult

class StudentReader(ABC):
    @abstractmethod
    def get_list(
        self,
        filters: StudentFilter,
        pagination: PaginationParams
    ) -> PagedResult[Student]:
        pass

    @abstractmethod
    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        pass
