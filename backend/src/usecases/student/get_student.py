
from src.domain.unit_of_work import IUnitOfWork
from src.domain.exceptions.student import StudentNotFoundError

class GetStudentUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, student_id: str) -> dict:
        with self.uow as uow:
            student = uow.students.get_by_student_id(student_id)
            
            if not student:
                raise StudentNotFoundError(student_id)
                
            # Convert to dictionary for XML Renderer
            return student.__dict__