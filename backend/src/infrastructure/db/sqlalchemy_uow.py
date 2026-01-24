from sqlalchemy.orm import sessionmaker
# from src.domain.unit_of_work import IUnitOfWork
from src.adapters.repositories.sqlalchemy_student_repository import SqlAlchemyStudentRepository
from src.infrastructure.db.base_uow import BaseUnitOfWork

class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.students = SqlAlchemyStudentRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            super().__exit__(exc_type, exc_val, exc_tb)
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
