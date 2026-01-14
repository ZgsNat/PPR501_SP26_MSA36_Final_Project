# domain/repositories/student_writer.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.domain.entities.student import Student

class StudentWriter(ABC):
    @abstractmethod
    def create(self, student: Student) -> Student:
        pass

    @abstractmethod
    def update(
        self,
        student_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Student]:
        pass

    @abstractmethod
    def delete(self, student_id: str) -> bool:
        pass
