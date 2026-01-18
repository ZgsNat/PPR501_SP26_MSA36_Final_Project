# Student Management System - Group 06 (MSA36)

## 📝 Project Overview
This project is part of the **PPR501** course. It is a comprehensive student management platform that allows administrators to track student information, analyze academic performance, and automate data collection.

### 🎯 Specific Requirements (Group 6)
- **Frontend:** ReactJS
- **Backend:** FastAPI
- **Data Crawling:** Selenium (Web automation)
- **API Response:** XML format
- **Data Storage:** Sqlite (students.db)
- **Data Processing:** Pandas (Cleaning & Analysis)

---

## 🚀 Key Features
- **Student Management:** Full CRUD (Create, Read, Update, Delete) operations.
- **Data Import:** Pre-loaded with 100 student records.
- **Web Crawling:** Automated data collection using Selenium.
- **Advanced Analytics:** - Data cleaning and preprocessing with Pandas.
  - Comparative analysis: English vs. Math scores, Hometown vs. English proficiency, etc.
- **Flexible API:** Specialized endpoints returning data in XML format.

---

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| **Backend** | Python, FastAPI |
| **Frontend** | ReactJS, TailwindCSS/Bootstrap |
| **Automation** | Selenium |
| **Data Analysis** | Pandas, Openpyxl |
| **Data Format** | XML, JSON |

---

## 📂 Project Structure
```text
├── README.md                       # Project overview and setup notes
├──backend/
│  ├── src/
│  │   ├── main.py                          # FastAPI application entry point
│  │   │
│  │   ├── domain/                          # 🏢 DOMAIN LAYER (Business Logic)
│  │   │   ├── entities/
│  │   │   │   └── student.py              # Student business entity
│  │   │   ├── repositories/
│  │   │   │   └── student_repository.py   # Repository interface (abstract)
│  │   │   ├── exceptions/                 # Domain-specific exceptions package
│  │   │   │   ├── __init__.py
│  │   │   │   ├── base.py                 # Base domain exception types
│  │   │   │   └── student.py              # Student-specific exceptions
│  │   │   └── unit_of_work.py             # Unit of Work interface
│  │   │
│  │   ├── usecases/                        # 📱 USE CASES LAYER (Application Logic)
│  │   │   └── student/
│  │   │       ├── create_student.py       # Create new student use case
│  │   │       ├── get_student.py          # Get single student use case
│  │   │       ├── list_students.py        # List all students with filtering
│  │   │       ├── update_student.py       # Update student data use case
│  │   │       └── delete_student.py       # Delete student use case
│  │   │
│  │   ├── adapters/                        # 🖥️  ADAPTERS LAYER (Interface)
│  │   │   ├── api/
│  │   │   │   ├── exception_handlers.py   # Central FastAPI exception handlers
│  │   │   │   └── student_controller.py   # FastAPI route handlers
│  │   │   ├── repositories/
│  │   │   │   └── sqlalchemy_student_repository.py  # ORM implementation
│  │   │   └── schemas/
│  │   │       └── student_schema.py       # Pydantic request/response schemas
│  │   │
│  │   ├── infrastructure/                  # 🔧 INFRASTRUCTURE LAYER
│  │   │   ├── db/
│  │   │   │   ├── database.py             # SQLAlchemy setup, session management
│  │   │   │   ├── mixins.py               # Base model mixins (timestamps)
│  │   │   │   └── sqlalchemy_uow.py       # Unit of Work implementation
│  │   │   ├── xml/
│  │   │   │   └── xml_renderer.py         # XML response formatter
│  │   │
│  │   └── shared/
│  │       └── pagination.py               # Pagination utilities
│  │
│  ├── Dockerfile                           # Docker container configuration
│  ├── entrypoint.sh                        # Container startup script
│  ├── requirements.txt                     # Python dependencies
│  ├── seed.py                             # Database seeding script (100 test records)
│  └── README.md                           # This file
├── frontend/                       # React frontend application
│   ├── package.json                # Frontend dependencies & scripts
│   ├── README.md                   # Frontend notes and run instructions
│   ├── public/
│   │   └── index.html              # HTML shell served to the browser
│   └── src/
│       ├── index.js                # React app bootstrap
│       ├── App.js                  # Top-level app component / routes
│       ├── App.css                 # Global app styles
│       ├── api/
│       │   └── axiosClient.js      # Axios instance for API requests
│       ├── components/
│       │   ├── common/
│       │   └── students/
│       │       ├── StudentFormMUI.js # Material UI variant of the form
│       │       └── StudentTable.js # Table listing students
│       ├── hooks/
│       │   └── useStudents.js      # React hook: fetch + manage student state
│       ├── pages/
│       │   └── StudentDashboard.js # Page that composes student components
│       ├── services/
│       │   └── studentService.js   # Frontend API wrappers (calls backend)
│       └── utils/
│           └── xmlParser.js        # Parse XML API responses to JS objects
```
