from sqlalchemy.orm import sessionmaker
from src.domain.unit_of_work import IUnitOfWork
from src.adapters.repositories.sqlalchemy_student_repository import SqlAlchemyStudentRepository

class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        # 1. Mở một session mới
        self.session = self.session_factory()
        
        # 2. Khởi tạo các Repository với session này
        self.students = SqlAlchemyStudentRepository(self.session)
        
        # 3. Trả về chính nó để dùng trong block 'with'
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Tự động commit/rollback khi thoát khỏi block 'with'
        try:
            if exc_type:
                self.session.rollback()  # Có lỗi -> Rollback
            else:
                self.session.commit()    # Không lỗi -> Commit
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()         # Luôn đóng kết nối
            
    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()