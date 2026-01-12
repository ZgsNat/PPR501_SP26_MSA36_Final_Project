from dataclasses import dataclass
from typing import Generic, TypeVar, List, Any

T = TypeVar("T")

@dataclass
class PaginationParams:
    page: int = 1
    size: int = 10

    def __post_init__(self):
        if self.page < 1: self.page = 1
        if self.size < 1: self.size = 10
        if self.size > 100: self.size = 100

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

@dataclass
class PagedResult(Generic[T]):
    items: List[T]
    total_records: int
    page: int
    size: int
    total_pages: int

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams):
        import math
        total_pages = math.ceil(total / params.size) if params.size > 0 else 1
        return cls(
            items=items,
            total_records=total,
            page=params.page,
            size=params.size,
            total_pages=total_pages
        )

    def to_dict(self):
        # Helper để convert sang dict cho API response
        return {
            "metadata": {
                "page": self.page,
                "size": self.size,
                "total_records": self.total_records,
                "total_pages": self.total_pages
            },
            "items": [item.__dict__ if hasattr(item, "__dict__") else item for item in self.items]
        }