from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.student_entity import StudentEntity
from app.models.student_model import StudentCreate, StudentFilter
from app.models.common import PaginationParams

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list(self, filters: StudentFilter, pagination: PaginationParams):
        """
        Builds a dynamic SQL query based on filters and pagination.
        Returns: (list_of_students, total_count)
        """
        query = self.db.query(StudentEntity)

        # 1. Apply Filters dynamically
        if filters.keyword:
            # Similar to SQL: WHERE (full_name LIKE '%kw%' OR email LIKE '%kw%')
            search = f"%{filters.keyword}%"
            query = query.filter(or_(
                StudentEntity.full_name.ilike(search),
                StudentEntity.email.ilike(search)
            ))

        if filters.home_town:
            # Using ilike for case-insensitive match
            query = query.filter(StudentEntity.home_town.ilike(f"%{filters.home_town}%"))

        if filters.min_math is not None:
            query = query.filter(StudentEntity.math_score >= filters.min_math)

        # 2. Count total records (before pagination)
        total_records = query.count()

        # 3. Apply Pagination (Offset/Limit)
        # EF Equivalent: .Skip(skip).Take(take)
        skip = (pagination.page - 1) * pagination.size
        items = query.offset(skip).limit(pagination.size).all()

        return items, total_records

    def get_by_student_id(self, student_id: str):
        return self.db.query(StudentEntity).filter(StudentEntity.student_id == student_id).first()

    def create(self, student: StudentCreate):
        db_obj = StudentEntity(
            student_id=student.student_id,
            full_name=student.full_name,
            email=student.email,
            phone=student.phone,
            home_town=student.home_town,
            birth_date=student.birth_date,
            math_score=student.math_score,
            literature_score=student.literature_score,
            english_score=student.english_score
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: StudentEntity, updates: dict):
        # Allow bulk setting attributes
        for key, value in updates.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: StudentEntity):
        self.db.delete(db_obj)
        self.db.commit()