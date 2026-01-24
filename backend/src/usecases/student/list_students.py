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

    def execute(self, query):
        pagination = PaginationParams(
            page=query.page,
            size=query.size
        )

        filters = StudentFilter(
            keyword=query.keyword,
            home_town=query.home_town,
            min_math=query.min_math,
            min_literature=query.min_literature,
            min_english=query.min_english
        )

        with self.uow as uow:
            return uow.students.get_list(filters, pagination).to_dict()