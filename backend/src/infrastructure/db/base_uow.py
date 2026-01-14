from src.domain.unit_of_work import IUnitOfWork


class BaseUnitOfWork(IUnitOfWork):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
