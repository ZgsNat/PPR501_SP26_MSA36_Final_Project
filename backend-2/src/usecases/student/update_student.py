from src.domain.unit_of_work import IUnitOfWork
from src.domain.exceptions.student import StudentNotFoundError, InvalidStudentDataError

class UpdateStudentUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, student_id: str, update_data: dict):
        with self.uow as uow:
            # 1. Check exists
            existing_student = uow.students.get_by_student_id(student_id)
            if not existing_student:
                raise StudentNotFoundError(student_id)
            
            # 2. Clean data
            clean_updates = {k: v for k, v in update_data.items() if v is not None}
            if "student_id" in clean_updates:
                del clean_updates["student_id"]
                
            if not clean_updates:
                # Raise lỗi Domain thay vì trả về string "NO_UPDATE"
                raise InvalidStudentDataError("No fields provided to update")

            # 3. Update in Repo
            return uow.students.update(student_id, clean_updates)