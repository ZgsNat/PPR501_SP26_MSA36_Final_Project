from sqlalchemy import or_
from src.infrastructure.db.models.student_orm import StudentORM
from src.domain.entities.student import StudentFilter


class StudentFilterApplier:
    def apply(self, query, filters: StudentFilter):
        if filters.keyword:
            search = f"%{filters.keyword}%"
            query = query.filter(or_(
                StudentORM.full_name.ilike(search),
                StudentORM.email.ilike(search)
            ))

        if filters.home_town:
            query = query.filter(
                StudentORM.home_town.ilike(f"%{filters.home_town}%")
            )

        if filters.min_math is not None:
            query = query.filter(StudentORM.math_score >= filters.min_math)

        if filters.min_literature is not None:
            query = query.filter(StudentORM.literature_score >= filters.min_literature)

        if filters.min_english is not None:
            query = query.filter(StudentORM.english_score >= filters.min_english)

        return query
