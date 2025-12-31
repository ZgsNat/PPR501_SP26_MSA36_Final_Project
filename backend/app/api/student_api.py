from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.student_service import StudentService
from app.models.student_model import StudentCreate, StudentUpdate, StudentFilter
from app.models.common import PaginationParams
from app.utils.xml_renderer import XMLResponse

router = APIRouter()

@router.get("/students", tags=["Students"], response_class=XMLResponse)
def get_students(
    pagination: PaginationParams = Depends(),
    filters: StudentFilter = Depends(),
    db: Session = Depends(get_db)
):
    service = StudentService(db)
    return service.get_students(pagination, filters)

@router.get("/student/{student_id}", tags=["Students"], response_class=XMLResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    service = StudentService(db)
    student = service.get_student_detail(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/student", tags=["Students"], status_code=201, response_class=XMLResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    service = StudentService(db)
    result = service.create_student(student)
    if not result:
        raise HTTPException(status_code=409, detail="Student ID already exists")
    return {"message": "Student created", "student_id": result.student_id}

@router.put("/student/{student_id}", tags=["Students"], response_class=XMLResponse)
def update_student(student_id: str, student: StudentUpdate, db: Session = Depends(get_db)):
    service = StudentService(db)
    result = service.update_student(student_id, student)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if result == "NO_UPDATE":
        raise HTTPException(status_code=400, detail="No fields provided to update")
        
    return {"message": "Student updated", "student_id": result.student_id}

@router.delete("/student/{student_id}", tags=["Students"], status_code=204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    service = StudentService(db)
    ok = service.delete_student(student_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Student not found")
    return