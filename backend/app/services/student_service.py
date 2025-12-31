from sqlalchemy.orm import Session
from app.repositories.student_repository import StudentRepository
from app.models.student_model import StudentCreate, StudentUpdate, StudentFilter
from app.models.common import PaginationParams
import math

class StudentService:
    def __init__(self, db: Session):
        self.repo = StudentRepository(db)

    def get_students(self, pagination: PaginationParams, filters: StudentFilter):
        # 1. Fetch all data
        # (For 100 records, Python filtering is fine and flexible)
        students = self.repo.get_all()
        
        # Convert to dictionary list to handle filtering easily
        data = []
        for s in students:
            s_dict = s.__dict__.copy()
            s_dict.pop('_sa_instance_state', None)
            data.append(s_dict)

        # 2. Filtering Logic
        filtered_data = []
        for s in data:
            match = True
            # Keyword Filter (Name or Email)
            if filters.keyword:
                kw = filters.keyword.lower()
                name = (s.get('full_name') or "").lower()
                email = (s.get('email') or "").lower()
                if kw not in name and kw not in email:
                    match = False
            
            # Hometown Filter
            if filters.home_town:
                if (s.get('home_town') or "").lower() != filters.home_town.lower():
                    match = False
            
            # Math Score Filter
            if filters.min_math is not None:
                if (s.get('math_score') or 0) < filters.min_math:
                    match = False
            
            if match:
                filtered_data.append(s)

        # 3. Pagination Logic
        total_records = len(filtered_data)
        total_pages = math.ceil(total_records / pagination.size) if pagination.size > 0 else 1
        
        start = (pagination.page - 1) * pagination.size
        end = start + pagination.size
        page_items = filtered_data[start:end]

        return {
            "metadata": {
                "page": pagination.page,
                "size": pagination.size,
                "total_records": total_records,
                "total_pages": total_pages
            },
            "items": page_items
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