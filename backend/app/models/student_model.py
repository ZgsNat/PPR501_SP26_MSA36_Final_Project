from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    home_town: Optional[str] = None
    birth_date: Optional[str] = None # Added field
    math_score: Optional[float] = 0.0
    literature_score: Optional[float] = 0.0
    english_score: Optional[float] = 0.0
    
    @field_validator('birth_date')
    def validate_date_format(cls, v):
        if v:
            try:
                datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError("Date must be in dd/mm/yyyy format")
        return v

class StudentCreate(StudentBase):
    student_id: str

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    home_town: Optional[str] = None
    math_score: Optional[float] = None
    literature_score: Optional[float] = None
    english_score: Optional[float] = None

class StudentFilter(BaseModel):
    keyword: Optional[str] = Field(None, description="Search name/email")
    home_town: Optional[str] = None
    min_math: Optional[float] = None

