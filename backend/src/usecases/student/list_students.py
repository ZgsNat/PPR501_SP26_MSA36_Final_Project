import unicodedata
from src.domain.unit_of_work import IUnitOfWork
from src.domain.entities.student import StudentFilter
from src.shared.pagination import PaginationParams

class ListStudentsUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def _normalize(self, text: str) -> str:
        if text is None: return None
        return unicodedata.normalize('NFC', text)

    def execute(self, page: int, size: int, keyword: str = None, home_town: str = None, min_math: float = None):
        # 1. Prepare Inputs
        pagination = PaginationParams(page=page, size=size)
        filters = StudentFilter(
            keyword=self._normalize(keyword),
            home_town=self._normalize(home_town),
            min_math=min_math
        )

        # 2. Call Repository (enter context to initialize session)
        with self.uow as uow:
            paged_result = uow.students.get_list(filters, pagination)

        # 3. Return Dictionary (cho XML Response)
        return paged_result.to_dict()