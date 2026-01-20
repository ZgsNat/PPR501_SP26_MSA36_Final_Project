# Student Management System - Clean Architecture Backend

A production-grade backend API for managing student records, built with **Clean Architecture principles** and following **SOLID design patterns**. This project demonstrates best practices in layered architecture, dependency injection, and separation of concerns.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)

---

## 🎯 Overview

This is a **Student Management System** API that provides comprehensive CRUD operations for student records. The project is architected using **Clean Architecture**, ensuring:

- ✅ Independence from frameworks, databases, and UI
- ✅ Highly testable business logic
- ✅ Clear separation of concerns
- ✅ Maintainable and scalable codebase
- ✅ Well-structured dependency injection


## 🏗️ Architecture

This project follows **Clean Architecture** with 4 concentric layers:

```
┌─────────────────────────────────────────┐
│      🖥️  ADAPTERS (Interface Layer)     │
│   Controllers, Schemas, Repositories    │
├─────────────────────────────────────────┤
│   📱 USE CASES (Application Layer)      │
│     Business Logic & Orchestration      │
├─────────────────────────────────────────┤
│     🏢 DOMAIN (Business Layer)          │
│   Entities, Exceptions, Interfaces      │
├─────────────────────────────────────────┤
│  🔧 INFRASTRUCTURE (Framework Layer)    │
│    Database, XML, External Services     │
└─────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Examples |
|-------|---|---|
| **Domain** | Core business logic, entities, rules | Student entity, exceptions, repository interfaces |
| **Use Cases** | Application workflows, orchestration | ListStudents, CreateStudent, UpdateStudent |
| **Adapters** | External world interfaces | API routes, HTTP schemas, ORM repositories |
| **Infrastructure** | Technical implementation | Database drivers, XML rendering, sessions |

### Design Patterns Used

- **Repository Pattern** - Abstract data access
- **Unit of Work Pattern** - Transaction management
- **Dependency Injection** - Loose coupling
- **Use Case Pattern** - Single responsibility workflows
- **Strategy Pattern** - Pluggable implementations

---

## 📁 Project Structure

```
backend/
├── src/
│   ├── main.py                          # FastAPI application entry point
│   │
│   ├── domain/                          # 🏢 DOMAIN LAYER (Business Logic)
│   │   ├── entities/
│   │   │   └── student.py              # Student business entity
│   │   ├── repositories/
│   │   │   ├── student/
│   │   │   │   ├── student_write.py
│   │   │   │   └── student_read.py
│   │   │   └── student_repository.py   # Repository interface (abstract)
│   │   ├── exceptions/                 # Domain-specific exceptions package
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 # Base domain exception types
│   │   │   └── student.py              # Student-specific exceptions
│   │   └── unit_of_work.py             # Unit of Work interface
│   │
│   ├── usecases/                        # 📱 USE CASES LAYER (Application Logic)
│   │   └── student/
│   │       ├── create_student.py       # Create new student use case
│   │       ├── get_student.py          # Get single student use case
│   │       ├── list_students.py        # List all students with filtering
│   │       ├── update_student.py       # Update student data use case
│   │       └── delete_student.py       # Delete student use case
│   │
│   ├── adapters/                        # 🖥️  ADAPTERS LAYER (Interface)
│   │   ├── api/
│   │   │   ├── exception_handlers.py   # Central FastAPI exception handlers
│   │   │   └── student_controller.py   # FastAPI route handlers
│   │   ├── repositories/
│   │   │   └── sqlalchemy_student_repository.py  # ORM implementation
│   │   └── schemas/
│   │       └── student_schema.py       # Pydantic request/response schemas
│   │
│   ├── infrastructure/                  # 🔧 INFRASTRUCTURE LAYER
│   │   ├── db/
│   │   │   ├── database.py             # SQLAlchemy setup, session management
│   │   │   ├── mixins.py               # Base model mixins (timestamps)
│   │   │   └── sqlalchemy_uow.py       # Unit of Work implementation
│   │   ├── xml/
│   │   │   └── xml_renderer.py         # XML response formatter
│   │
│   └── shared/
│       └── pagination.py               # Pagination utilities
│
├── Dockerfile                           # Docker container configuration
├── entrypoint.sh                        # Container startup script
├── requirements.txt                     # Python dependencies
├── seed.py                             # Database seeding script (100 test records)
└── README.md                           # This file
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI |
| **Web Server** | Uvicorn |
| **ORM** | SQLAlchemy |
| **Database** | SQLite |
| **Data Validation** | Pydantic v2 |
| **XML Rendering** | dicttoxml |
| **Testing Data** | Faker, Pandas, openpyxl |
| **Containerization** | Docker |
| **Language** | Python 3.11 |

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- pip or conda
- (Optional) Docker

### Setup Steps

**1. Clone and navigate to project:**
```bash
cd backend
```

**2. Create virtual environment:**
```bash
python -m venv .venv
```

**3. Activate virtual environment:**

On Windows:
```bash
.venv\Scripts\Activate.ps1
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

**4. Install dependencies:**
```bash
pip install -r requirements.txt
```

**5. Seed the database:**
```bash
python seed.py
```
This creates `students.db` with 100 randomly generated test students.

---

## 🚀 Running the Application

### Development Mode (with auto-reload)

```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at: `http://127.0.0.1:8000`

### Interactive API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Using Docker

**Build image:**
```bash
docker build -t student-api .
```

**Run container:**
```bash
docker run -p 8000:8000 student-api
```

---

## 📡 API Endpoints

All responses are returned in **XML format** by default.

## ⚠️ Exception Flow

This project centralizes error handling so teammates can quickly understand how exceptions travel from the domain to HTTP/XML responses:

- Domain raises typed exceptions (see `src/domain/exceptions/`): `base.py` defines common base types and `student.py` contains student-specific errors.
- Use cases propagate domain errors for business-level problems (e.g., not found, validation failures).
- Repository or DB layers may raise infrastructure errors (integrity, connection). The Unit of Work (`src/infrastructure/db/sqlalchemy_uow.py`) ensures transactions are rolled back on exceptions.
- The API layer (`src/adapters/api/exception_handlers.py`) registers FastAPI exception handlers that map domain/infrastructure exceptions to appropriate HTTP status codes (e.g., 404 Not Found, 400 Bad Request, 409 Conflict, 500 Internal Server Error) and serialize responses to XML using the project's XML renderer.

Notes for contributors:

- To add a new domain error, create it under `src/domain/exceptions/` and add a mapping in `src/adapters/api/exception_handlers.py`.
- Handlers should return structured error payloads (code, message, details) so the XML responses remain consistent and machine-parsable.

