from src.domain.unit_of_work import IUnitOfWork  # Import Interface
from src.domain.exceptions.student import StudentNotFoundError

class DeleteStudentUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, student_id: str):
        with self.uow as uow:
            # Repo trả về True nếu xóa thành công, False nếu không tìm thấy
            is_deleted = uow.students.delete(student_id)
            
            if not is_deleted:
                raise StudentNotFoundError(student_id)
                
        return True