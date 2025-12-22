# Student Management System - Group 06 (MSA36)

## 📝 Project Overview
This project is part of the **PPR501** course. It is a comprehensive student management platform that allows administrators to track student information, analyze academic performance, and automate data collection.

### 🎯 Specific Requirements (Group 6)
- **Frontend:** ReactJS
- **Backend:** FastAPI
- **Data Crawling:** Selenium (Web automation)
- **API Response:** XML format
- **Data Storage:** Excel (.xlsx)
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
├── backend/            # FastAPI Source Code
│   ├── main.py         # Entry point
│   ├── models/         # Data schemas
│   ├── scraper/        # Selenium crawler scripts
│   └── data/           # Excel storage files
├── frontend/           # ReactJS Source Code
│   ├── src/components/ # UI Components
│   └── src/pages/      # Application views
└── analysis/           # Jupyter Notebooks/Pandas scripts for data insights
