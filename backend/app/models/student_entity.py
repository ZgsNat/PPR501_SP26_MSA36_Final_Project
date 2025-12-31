from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class StudentEntity(Base):
    __tablename__ = "students"

    # Auto-incrementing ID for DB performance
    id = Column(Integer, primary_key=True, index=True)
    
    # The actual Student ID (SV1001)
    student_id = Column(String, unique=True, index=True, nullable=False)
    
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    home_town = Column(String, nullable=True)
    birth_date = Column(String, nullable=True) 
    math_score = Column(Float, default=0.0)
    literature_score = Column(Float, default=0.0)
    english_score = Column(Float, default=0.0)