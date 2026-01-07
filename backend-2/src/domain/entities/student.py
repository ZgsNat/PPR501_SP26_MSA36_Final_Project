from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Student:
    student_id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    home_town: Optional[str] = None
    birth_date: Optional[str] = None
    math_score: float = 0.0
    literature_score: float = 0.0
    english_score: float = 0.0
    id: Optional[int] = None

    def validate_birth_date(self):
        if self.birth_date:
            try:
                datetime.strptime(self.birth_date, '%d/%m/%Y')
            except ValueError:
                raise ValueError("Date must be in dd/mm/yyyy format")

# Filter Object - Platform agnostic
@dataclass
class StudentFilter:
    keyword: Optional[str] = None
    home_town: Optional[str] = None
    min_math: Optional[float] = None