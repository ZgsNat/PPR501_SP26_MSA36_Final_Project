from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

# Input Schema
class StudentCreateSchema(BaseModel):
    student_id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    home_town: Optional[str] = None
    birth_date: Optional[str] = None
    math_score: float = 0.0
    literature_score: float = 0.0
    english_score: float = 0.0

    @field_validator('birth_date')
    def validate_date(cls, v):
        if v:
            datetime.strptime(v, '%d/%m/%Y')
        return v

class StudentUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    home_town: Optional[str] = None
    math_score: Optional[float] = None
    literature_score: Optional[float] = None
    english_score: Optional[float] = None