from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Creates a file 'students.db' in your project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"

# connect_args is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency Injection for API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()