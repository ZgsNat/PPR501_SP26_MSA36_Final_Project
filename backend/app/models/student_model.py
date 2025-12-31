from pydantic import BaseModel, Field
from typing import Optional

class StudentBase(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    home_town: Optional[str] = None
    birth_date: Optional[str] = None # Added field
    math_score: Optional[float] = 0.0
    literature_score: Optional[float] = 0.0
    english_score: Optional[float] = 0.0

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