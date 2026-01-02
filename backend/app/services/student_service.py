from sqlalchemy.orm import Session
from app.repositories.student_repository import StudentRepository
from app.models.student_model import StudentCreate, StudentUpdate, StudentFilter
from app.models.common import PaginationParams
import math
import unicodedata

class StudentService:
    def __init__(self, db: Session):
        self.repo = StudentRepository(db)

    def _normalize(self, text: str) -> str:
        """Converts typed Vietnamese into a standard format (NFC)"""
        if text is None:
            return None
        return unicodedata.normalize('NFC', text)
    
    def get_students(self, pagination: PaginationParams, filters: StudentFilter):
        filters.keyword = self._normalize(filters.keyword)
        filters.home_town = self._normalize(filters.home_town)
        # 1. Delegate filtering & sorting to the Database
        students_entities, total_records = self.repo.get_list(filters, pagination)

        # 2. Calculate Metadata
        total_pages = math.ceil(total_records / pagination.size) if pagination.size > 0 else 1

        # 3. Convert Entities to Dictionaries (or Pydantic Models)
        data = []
        for s in students_entities:
            # Ideally, use Pydantic: StudentRead.model_validate(s)
            s_dict = s.__dict__.copy()
            s_dict.pop('_sa_instance_state', None)
            data.append(s_dict)

        return {
            "metadata": {
                "page": pagination.page,
                "size": pagination.size,
                "total_records": total_records,
                "total_pages": total_pages
            },
            "items": data
        }

    def get_student_detail(self, student_id: str):
        s = self.repo.get_by_student_id(student_id)
        if s:
            res = s.__dict__.copy()
            res.pop('_sa_instance_state', None)
            return res
        return None

    def create_student(self, student: StudentCreate):
        if self.repo.get_by_student_id(student.student_id):
            return None # Conflict
        return self.repo.create(student)

    def update_student(self, student_id: str, student_update: StudentUpdate):
        db_student = self.repo.get_by_student_id(student_id)
        if not db_student:
            return None
        
        updates = student_update.model_dump(exclude_unset=True)
        if "student_id" in updates: 
            del updates["student_id"] # Prevent ID change
            
        if not updates:
            return "NO_UPDATE"

        return self.repo.update(db_student, updates)

    def delete_student(self, student_id: str):
        db_student = self.repo.get_by_student_id(student_id)
        if not db_student:
            return False
        self.repo.delete(db_student)
        return True