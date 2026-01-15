from sqlalchemy import Column, Integer, String, Float
from src.infrastructure.db.database import Base
from src.infrastructure.db.mixins import TimestampMixin, SoftDeleteMixin
from src.domain.entities.student import Student


class StudentORM(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    home_town = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)

    math_score = Column(Float, nullable=True)
    literature_score = Column(Float, nullable=True)
    english_score = Column(Float, nullable=True)

    def to_domain(self) -> Student:
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
            english_score=self.english_score,
        )
