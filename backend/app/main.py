from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import student_api
from app.core.database import engine, Base
import uvicorn

# Create Database Tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System - Group 6")

# CORS (Allow Frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_api.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to API Group 6 (XML Response)"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)