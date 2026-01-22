from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.domain.exceptions.student import InvalidStudentDataError

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

    def __post_init__(self):
        # self.validate_birth_date()
        # self.validate_scores() 
        pass
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.validate()

    def validate(self, validator = None):
        if validator:
            validator.validate()
        else:
            self._default_validate()
                
    def _default_validate(self):
        self.validate_birth_date()
        self.validate_scores()

    def validate_birth_date(self):
        if self.birth_date:
            try:
                datetime.strptime(self.birth_date, '%d/%m/%Y')
            except ValueError:
                raise InvalidStudentDataError(f"Date must be in dd/mm/yyyy format. Got: {self.birth_date}")

    def validate_scores(self):
        scores = [self.math_score, self.literature_score, self.english_score]
        for score in scores:
            if score is not None and (score < 0 or score > 10):
                raise InvalidStudentDataError(f"Score must be between 0 and 10. Got: {score}")
@dataclass
class StudentFilter:
    keyword: Optional[str] = None
    home_town: Optional[str] = None
    min_math: Optional[float] = None
    min_literature: Optional[float] = None
    min_english: Optional[float] = None