from pydantic import BaseModel, Field
from typing import Optional

class StudentQueryDTO(BaseModel):
    # Pagination (API concern)
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

    # Filters (API representation)
    keyword: Optional[str] = None
    home_town: Optional[str] = None

    min_math: Optional[float] = None
    min_literature: Optional[float] = None
    min_english: Optional[float] = None
