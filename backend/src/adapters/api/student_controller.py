from fastapi import APIRouter, Depends, Query, status
from src.infrastructure.xml.xml_renderer import XMLResponse

# Infrastructure & UoW
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.sqlalchemy_uow import SqlAlchemyUnitOfWork

# Schemas
from src.adapters.schemas.student_schema import StudentCreateSchema, StudentUpdateSchema
from src.adapters.schemas.student_query import StudentQueryDTO

# Use Cases
from src.usecases.student.list_students import ListStudentsUseCase
from src.usecases.student.get_student import GetStudentUseCase
from src.usecases.student.create_student import CreateStudentUseCase
from src.usecases.student.update_student import UpdateStudentUseCase
from src.usecases.student.delete_student import DeleteStudentUseCase

# Domain validator
from src.domain.service.student_validator import (
    DefaultStudentValidator,
    InternalStudentValidator
)

router = APIRouter()

# --- Dependency Injection Helper ---
# Thay vì lấy db session, ta lấy hẳn một Unit of Work
def get_uow():
    return SqlAlchemyUnitOfWork(SessionLocal)

# --- Routes ---

@router.get("/students", response_class=XMLResponse)
def list_students(
    query: StudentQueryDTO = Depends(),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    uc = ListStudentsUseCase(uow)
    return uc.execute(query)


@router.get("/student/{student_id}", response_class=XMLResponse)
def get_student(
    student_id: str, 
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    """
    Lấy chi tiết sinh viên.
    Nếu không tìm thấy, UseCase sẽ raise StudentNotFoundError -> Middleware trả 404.
    """
    uc = GetStudentUseCase(uow)
    return uc.execute(student_id)


@router.post("/student", status_code=status.HTTP_201_CREATED, response_class=XMLResponse)
def create_student(
    student_in: StudentCreateSchema, 
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    # this is only for demo purpose
    # in real world, you can choose either DefaultStudentValidator or InternalStudentValidator
    # based on your business logic or configuration
    # we need to use design pattern like Factory Pattern to make it more elegant
    # Composite Pattern can also be used if multiple validators are needed
    # or you can divide into different endpoints for different validation strategies
    # Fastapi Dependency Injection can also be used to inject different validators
    # based on request context or user roles
    validator = DefaultStudentValidator()

    uc = CreateStudentUseCase(uow, validator)
    result = uc.execute(student_in.model_dump())
    return {"message": "Student created", "student_id": result.student_id}


@router.put("/student/{student_id}", response_class=XMLResponse)
def update_student(
    student_id: str, 
    student_in: StudentUpdateSchema, 
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    """
    Cập nhật thông tin sinh viên.
    exclude_unset=True để chỉ update những trường người dùng gửi lên.
    """
    uc = UpdateStudentUseCase(uow)
    result = uc.execute(student_id, student_in.model_dump(exclude_unset=True))
    return {"message": "Student updated", "student_id": result.student_id}


@router.delete("/student/{student_id}", response_class=XMLResponse)
def delete_student(
    student_id: str, 
    uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    """
    Xóa sinh viên (Soft Delete).
    """
    uc = DeleteStudentUseCase(uow)
    uc.execute(student_id)
    return {"message": "Student deleted", "student_id": student_id}