**Student Management System (Backend)**

**Project Overview**:
- **Description**: Backend API for a Student Management System that exposes REST endpoints returning XML responses.
- **Tech stack**: FastAPI, SQLAlchemy (SQLite), Pydantic, dicttoxml, Uvicorn.

**Architecture**
- **Pattern**: Layered architecture (API -> Service -> Repository -> Database)
- Diagram:

    Client (HTTP) 
         |
      FastAPI
    [app/main.py]
         |
    Router: [app/api/student_api.py]
         |
    Service layer: [app/services/student_service.py]
         |
    Repository layer: [app/repositories/student_repository.py]
         |
    Persistence: [app/core/database.py] -> SQLite (`students.db`)

**Components**
- **API**: `GET /api/v1/students`, `GET /api/v1/student/{id}`, `POST /api/v1/student`, `PUT /api/v1/student/{id}`, `DELETE /api/v1/student/{id}` — implemented in [app/api/student_api.py](app/api/student_api.py).
- **Service**: Business logic, filtering, pagination and orchestration — [app/services/student_service.py](app/services/student_service.py).
- **Repository**: Direct DB access using SQLAlchemy ORM — [app/repositories/student_repository.py](app/repositories/student_repository.py).
- **Models / Entities**: Pydantic request/response models and SQLAlchemy entity definitions — [app/models/student_model.py](app/models/student_model.py), [app/models/student_entity.py](app/models/student_entity.py), [app/models/common.py](app/models/common.py).
- **Database core**: SQLAlchemy engine, `SessionLocal`, and DI dependency `get_db()` — [app/core/database.py](app/core/database.py).
- **XML Renderer**: Custom response class that converts dicts to XML using `dicttoxml` — [app/utils/xml_renderer.py](app/utils/xml_renderer.py).
- **Seed data**: `seed.py` to populate `students.db` with sample data.

````markdown
**Student Management System — Backend**

Brief: This repository implements a FastAPI backend that manages student records and exposes a small REST API which returns XML responses by default. It provides CRUD operations, basic filtering/pagination, input validation, and persistence using SQLAlchemy with an SQLite database.

Primary responsibilities
- Expose HTTP endpoints to create, read, update, and delete student records.
- Validate and map request payloads with Pydantic models.
- Orchestrate business rules in the service layer (filtering, pagination, basic validation beyond schema).
- Persist domain entities via a repository layer implemented with SQLAlchemy.
- Return responses as XML using a custom XML response renderer.

Core files and roles
- `app/main.py`: FastAPI application and router mounting.
- `app/api/student_api.py`: HTTP route handlers (controllers) for student endpoints.
- `app/services/student_service.py`: Business-use-case implementations (list, get, create, update, delete).
- `app/repositories/student_repository.py`: DB access layer using SQLAlchemy ORM.
- `app/core/database.py`: Engine, session factory (`SessionLocal`) and DB initialization.
- `app/models/*`: Pydantic request/response models and SQLAlchemy entity definitions.
- `app/utils/xml_renderer.py`: Converts Python dicts/lists to XML responses.
- `seed.py`: Optional helper to populate the DB with sample data.

Available endpoints (base path `/api/v1`)
- `GET /students` — list students (supports pagination/filter query params).
- `GET /student/{id}` — fetch a single student by id.
- `POST /student` — create a new student.
- `PUT /student/{id}` — update an existing student.
- `DELETE /student/{id}` — delete a student.

Run locally (Windows)
1. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. (Optional) Seed sample data:

```powershell
python seed.py
```

4. Start server:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Notes & considerations
- Responses default to XML via `XMLResponse` in `app/utils/xml_renderer.py`. The codebase can be extended to support JSON content negotiation.
- The current project structure follows a pragmatic layered pattern (API → Service → Repository → DB). It is intentionally simple to keep the learning surface small.

````