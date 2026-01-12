from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.adapters.api import student_controller
from src.adapters.api.exception_handlers import register_exception_handlers
from src.infrastructure.db.database import engine, Base
import uvicorn

app = FastAPI(title="Student Management System - Clean Arch")

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_controller.router, prefix="/api/v1", tags=["Students"])

@app.get("/")
def read_root():
    return {"message": "Welcome to API Group 6 (XML Response)"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
