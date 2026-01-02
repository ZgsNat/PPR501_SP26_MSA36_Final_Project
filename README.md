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
├── backend/                        # FastAPI backend and data logic
│   ├── README.md                   # Backend-specific notes and run instructions
│   ├── requirements.txt            # Python dependencies for backend
│   ├── seed.py                     # Script to populate initial Excel student data
│   └── app/
│       ├── main.py                 # FastAPI application entrypoint (routes mount)
│       ├── api/
│       │   └── student_api.py      # API endpoints for student CRUD (returns XML)
│       ├── core/
│       │   └── database.py         # Excel storage access and DB-like helpers
│       ├── models/
│       │   ├── common.py           # Shared constants/types
│       │   ├── student_entity.py   # Internal student entity representation
│       │   └── student_model.py    # Pydantic models / request & response schemas
│       ├── repositories/
│       │   └── student_repository.py # Data access layer (CRUD using Excel)
│       ├── services/
│       │   └── student_service.py  # Business logic and validation
│       └── utils/
│           └── xml_renderer.py     # Helper to render API responses as XML
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
│       │   │   ├── Modal.js        # Reusable modal component
│       │   │   └── Pagination.js   # Pagination UI component
│       │   └── students/
│       │       ├── StudentFilter.js# Filter controls for student list
│       │       ├── StudentForm.js  # Student create/edit form (vanilla)
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
