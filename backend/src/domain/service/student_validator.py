from abc import ABC, abstractmethod
from src.domain.entities.student import Student
from src.domain.exceptions.student import InvalidStudentDataError

class StudentValidator(ABC):
    @abstractmethod
    def validate(self, student: Student) -> None:
        pass

class DefaultStudentValidator(StudentValidator):
    def validate(self, student: Student) -> None:
        student.validate_birth_date()
        student.validate_scores()

class InternalStudentValidator(StudentValidator):
    def validate(self, student: Student) -> None:
        student.validate_birth_date()
        if student.english_score < 6:
            raise InvalidStudentDataError("English >= 6 required")