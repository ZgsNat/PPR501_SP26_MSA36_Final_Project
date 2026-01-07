from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, or_
from src.infrastructure.db.database import Base
from src.infrastructure.db.mixins import TimestampMixin, SoftDeleteMixin
from src.domain.entities.student import Student, StudentFilter
from src.domain.repositories.student_repository import IStudentRepository
from src.shared.pagination import PaginationParams, PagedResult
from typing import Optional, Dict, Any

# --- ORM Model ---
class StudentORM(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    home_town = Column(String, nullable=True)
    birth_date = Column(String, nullable=True) 
    math_score = Column(Float, default=0.0)
    literature_score = Column(Float, default=0.0)
    english_score = Column(Float, default=0.0)

    def to_domain(self) -> Student:
        # Mapping từ ORM -> Domain Entity
        return Student(
            id=self.id,
            student_id=self.student_id,
            full_name=self.full_name,
            email=self.email,
            phone=self.phone,
            home_town=self.home_town,
            birth_date=self.birth_date,
            math_score=self.math_score,
            literature_score=self.literature_score,
            english_score=self.english_score
        )

class SqlAlchemyStudentRepository(IStudentRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_list(self, filters: StudentFilter, pagination: PaginationParams) -> PagedResult[Student]:
        query = self.db.query(StudentORM)
        
        query = query.filter(StudentORM.deleted_at == None)
        # --- Apply Generic Filters Logic Here ---
        if filters.keyword:
            search = f"%{filters.keyword}%"
            query = query.filter(or_(
                StudentORM.full_name.ilike(search),
                StudentORM.email.ilike(search)
            ))
            
        if filters.home_town:
            query = query.filter(StudentORM.home_town.ilike(f"%{filters.home_town}%"))
            
        if filters.min_math is not None:
            query = query.filter(StudentORM.math_score >= filters.min_math)

        # --- Pagination Logic ---
        total_records = query.count()
        items_orm = query.offset(pagination.offset).limit(pagination.size).all()
        
        # Convert List[ORM] -> List[Entity]
        items_domain = [item.to_domain() for item in items_orm]
        
        return PagedResult.create(items_domain, total_records, pagination)

    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        orm = self.db.query(StudentORM).filter(StudentORM.student_id == student_id and
                                               StudentORM.deleted_at == None).first()
        return orm.to_domain() if orm else None

    def create(self, student: Student) -> Student:
        orm = StudentORM(
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
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return orm.to_domain()

    def update(self, student_id: str, updates: Dict[str, Any]) -> Optional[Student]:
        orm = self.db.query(StudentORM).filter(StudentORM.student_id == student_id).first()
        if not orm:
            return None
        
        for key, value in updates.items():
            if hasattr(orm, key):
                setattr(orm, key, value)
        
        self.db.commit()
        self.db.refresh(orm)
        return orm.to_domain()

    def delete(self, student_id: str) -> bool:
        # orm = self.db.query(StudentORM).filter(StudentORM.student_id == student_id).first()
        # if not orm:
        #     return False
        # self.db.delete(orm)
        # self.db.commit()
        # return True
        orm = self.db.query(StudentORM).filter(StudentORM.student_id == student_id).first()
        if not orm:
            return False

        orm.deleted_at = datetime.now()
        self.db.commit()
        return True