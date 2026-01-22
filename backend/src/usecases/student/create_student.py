from src.domain.unit_of_work import IUnitOfWork  # Import Interface
from src.domain.entities.student import Student
from src.domain.service.student_validator import StudentValidator
from src.domain.exceptions.student import StudentAlreadyExistsError, InvalidStudentDataError
from datetime import datetime

class CreateStudentUseCase:
    def __init__(self, uow: IUnitOfWork, validator: StudentValidator):
        self.uow = uow
        self.validator = validator

    def execute(self, data: dict) -> Student:
        # Sử dụng context manager (with) để đảm bảo transaction 
        with self.uow as uow:
            # Truy cập repo thông qua uow.students
            if uow.students.get_by_student_id(data['student_id']):
                raise StudentAlreadyExistsError(data['student_id'])
            
            new_student = Student(**data)
            self.validator.validate(new_student)
            # new_student = Student(**data)
            # new_student.validate_birth_date()
            # new_student.validate_scores()
            created_student = uow.students.create(new_student)
            
            return created_student