from datetime import datetime
from sqlalchemy.orm import Session
from src.domain.entities.student import Student, StudentFilter
from src.domain.repositories.student_repository import IStudentRepository
from src.infrastructure.db.student_filter_applier import StudentFilterApplier
from src.infrastructure.db.models.student_orm import StudentORM
from src.shared.pagination import PaginationParams, PagedResult
from typing import Optional, Dict, Any


# class SqlAlchemyStudentRepository(IStudentRepository):
#     def __init__(self, db: Session):
#         self.db = db

#     def get_list(self, filters: StudentFilter, pagination: PaginationParams) -> PagedResult[Student]:
#         query = self.db.query(StudentORM)
        
#         query = query.filter(StudentORM.deleted_at == None)
#         # --- Apply Generic Filters Logic Here ---
#         if filters.keyword:
#             search = f"%{filters.keyword}%"
#             query = query.filter(or_(
#                 StudentORM.full_name.ilike(search),
#                 StudentORM.email.ilike(search)
#             ))
            
#         if filters.home_town:
#             query = query.filter(StudentORM.home_town.ilike(f"%{filters.home_town}%"))
            
#         if filters.min_math is not None:
#             query = query.filter(StudentORM.math_score >= filters.min_math)

#         # --- Pagination Logic ---
#         total_records = query.count()
#         items_orm = query.offset(pagination.offset).limit(pagination.size).all()
        
#         # Convert List[ORM] -> List[Entity]
#         items_domain = [item.to_domain() for item in items_orm]
        
#         return PagedResult.create(items_domain, total_records, pagination)
class SqlAlchemyStudentRepository(IStudentRepository):
    def __init__(self, db: Session):
        self.db = db
        self.filter_applier = StudentFilterApplier()

    def get_list(
        self,
        filters: StudentFilter,
        pagination: PaginationParams
    ) -> PagedResult[Student]:

        query = self.db.query(StudentORM)
        query = query.filter(StudentORM.deleted_at == None)

        query = self.filter_applier.apply(query, filters)

        total = query.count()
        items = (
            query
            .offset(pagination.offset)
            .limit(pagination.size)
            .all()
        )

        students = [item.to_domain() for item in items]

        return PagedResult.create(students, total, pagination)

    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        orm = self.db.query(StudentORM).filter((StudentORM.student_id == student_id) &
                                               (StudentORM.deleted_at == None)).first()
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
        orm = self.db.query(StudentORM).filter((StudentORM.student_id == student_id) &
                                               (StudentORM.deleted_at == None)).first()
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
        orm = self.db.query(StudentORM).filter((StudentORM.student_id == student_id) &
                                               (StudentORM.deleted_at == None)).first()
        if not orm:
            return False

        orm.deleted_at = datetime.now()
        self.db.commit()
        return True