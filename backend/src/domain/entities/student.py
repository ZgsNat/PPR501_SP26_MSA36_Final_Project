from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.domain.exceptions.student import InvalidStudentDataError

@dataclass
class Student:
    # 1. KHAI BÁO CÁC TRƯỜNG DỮ LIỆU TRƯỚC (QUAN TRỌNG)
    # Dataclass sẽ nhìn vào đây để tự tạo hàm __init__(student_id, full_name, ...)
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

    # 2. DÙNG __post_init__ ĐỂ VALIDATE TỰ ĐỘNG
    # Hàm này được Python tự động gọi SAU KHI đã gán xong các giá trị ở trên
    def __post_init__(self):
        # self.validate_birth_date()
        # self.validate_scores() # Nếu bạn muốn check điểm luôn
        pass
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Validate invariant sau khi update
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
        # Validate điểm số logic nghiệp vụ (0-10)
        scores = [self.math_score, self.literature_score, self.english_score]
        for score in scores:
            if score is not None and (score < 0 or score > 10):
                raise InvalidStudentDataError(f"Score must be between 0 and 10. Got: {score}")

# Filter Object - Giữ nguyên
@dataclass
class StudentFilter:
    keyword: Optional[str] = None
    home_town: Optional[str] = None
    min_math: Optional[float] = None
    min_literature: Optional[float] = None
    min_english: Optional[float] = None