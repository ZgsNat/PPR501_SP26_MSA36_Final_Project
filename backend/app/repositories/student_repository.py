from sqlalchemy.orm import Session
from app.models.student_entity import StudentEntity
from app.models.student_model import StudentCreate

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(StudentEntity).all()

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
        for key, value in updates.items():
            setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: StudentEntity):
        self.db.delete(db_obj)
        self.db.commit()