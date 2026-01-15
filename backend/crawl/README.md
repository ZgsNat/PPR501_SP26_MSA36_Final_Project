# Student Data Crawler - Selenium Web Scraper

Selenium script to crawl student data from the Student Management System web application.

## Overview

This crawler automatically extracts student records from the frontend application running on `http://localhost:3000`. It supports pagination to crawl all available data and exports results in multiple formats.

## What Data is Crawled

The crawler extracts the following information:

### Student Records (11 columns):
1. **student_id** - Student ID (e.g., SV1001)
2. **full_name** - Full name of the student
3. **birth_date** - Date of birth
4. **phone** - Phone number
5. **email** - Email address
6. **home_town** - Hometown/city
7. **math_score** - Mathematics score (0-10)
8. **literature_score** - Literature score (0-10)
9. **english_score** - English score (0-10)
10. **average_score** - Average score (calculated)
11. **actions** - Action buttons (Edit/Delete)

### Additional Metadata:
- **Table structure** - Column names and count
- **Page metadata** - Title, URL, total records, pagination info
- **Crawl timestamp** - When the data was collected
- **Screenshots** - Visual proof of crawl execution

## Output Files

After running the crawler, the following files are generated in the `crawl_data/` directory:

### 1. JSON Format (`crawled_data.json`)
Complete structured data including:
- All student records
- Table structure information
- Page metadata
- Timestamps

**Use case**: API integration, data processing, backup

### 2. Excel Format (`crawled_data.xlsx`)
Multi-sheet workbook containing:
- **Sheet 1 (Students)**: All student records in tabular format
- **Sheet 2 (Metadata)**: Page and crawl information
- **Sheet 3 (Table Structure)**: Column definitions

**Use case**: Data analysis, reporting, sharing with non-technical users

### 3. CSV Format (`crawled_data.csv`)
Flat file with student records only.

**Use case**: Import to databases, spreadsheet applications, data science tools

### 4. Screenshots
- **page_loaded.png** - Screenshot after page loads
- **crawl_complete.png** - Screenshot after crawl completes

**Use case**: Visual verification, debugging, documentation

## How to Run

### Prerequisites

1. **Python environment** - Ensure you're in the backend virtual environment
2. **ChromeDriver** - Must be installed and match your Chrome version
3. **Frontend running** - Application must be accessible at `http://localhost:3000`
4. **Backend running** - API must be running on `http://127.0.0.1:8000`

### Installation

Install required packages:

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (Windows)
.\.venv\Scripts\Activate.ps1

# Install Selenium (if not already installed)
pip install selenium
```

### Running the Crawler

```bash
# Navigate to crawl directory
cd crawl

# Run the crawler
python selenium_crawler.py
```

### Expected Output

```
============================================================
  Student Management System - Web Crawler
============================================================
✓ WebDriver initialized successfully

→ Navigating to http://localhost:3000...
✓ Successfully loaded: React App
✓ Screenshot saved: crawl_data/page_loaded.png

→ Setting rows per page to 100...
  Found dropdown using selector: //div[contains(@class, 'MuiTablePagination-select')]
  Selected 100 rows per page
✓ Successfully set to 100 rows per page

→ Extracting table structure...
  Found 11 columns
✓ Table structure extracted

→ Crawling all pages...
  Found 100 rows using selector: //div[contains(@class, 'MuiDataGrid-row')]
  Total records: 400, Pages: 4

  → Moving to page 2/4...
  Found 100 rows...
  
  → Moving to page 3/4...
  Found 100 rows...
  
  → Moving to page 4/4...
  Found 100 rows...

✓ Total crawled: 400 records from 4 page(s)

============================================================
  Saving Data
============================================================
✓ Data saved to JSON: crawl_data/crawled_data.json
✓ Data saved to Excel: crawl_data/crawled_data.xlsx
✓ Data saved to CSV: crawl_data/crawled_data.csv
✓ Screenshot saved: crawl_data/crawl_complete.png

============================================================
  Crawl Summary
============================================================
  Total records crawled: 400
  Columns found: 11
  Page title: React App
============================================================

→ Closing browser...
✓ Browser closed

✓ Crawling completed successfully!
```

## Advanced Usage

### Custom Configuration

```python
from selenium_crawler import StudentDataCrawler

# Create crawler with custom settings
crawler = StudentDataCrawler(
    base_url="http://localhost:3000",  # Change URL if needed
    headless=True,                      # Run without browser UI
    output_dir="my_custom_folder"       # Custom output directory
)

# Run with specific formats
crawler.crawl(save_formats=['json', 'excel'])  # Only JSON and Excel

# Get data programmatically
data = crawler.get_data()
print(f"Crawled {len(data['students'])} students")
```

### Headless Mode (No Browser UI)

For faster execution or server environments:

```python
crawler = StudentDataCrawler(headless=True)
crawler.crawl()
```

## 🔧 Performance Optimizations

The crawler includes several optimizations:

- **Disabled image loading** - Faster page loads
- **Reduced wait times** - Optimized for speed
- **Parallel processing** - Efficient data extraction
- **Smart pagination** - Automatic page detection

**Typical execution time**: 15-25 seconds for 400 records

## Data Quality

The crawler handles:

- Missing values (null, empty fields)
- Special characters in text
- Invalid scores (< 0 or > 10)
- Dynamic content loading
- Pagination edge cases

## Troubleshooting

### Common Issues

**1. "ChromeDriver not found"**
- Install ChromeDriver matching your Chrome version
- Add ChromeDriver to system PATH

**2. "Could not navigate to dashboard"**
- Ensure frontend is running on `http://localhost:3000`
- Check if backend API is accessible

**3. "No data rows found"**
- Verify the page has loaded completely
- Check if data exists in the database

**4. "Timeout errors"**
- Increase wait times in the script
- Check internet connection and system performance

## Directory Structure

```
backend/crawl/
├── selenium_crawler.py       # Main crawler script
├── README.md                  # This file
└── crawl_data/                # Output directory (auto-created)
    ├── crawled_data.json      # JSON output
    ├── crawled_data.xlsx      # Excel output
    ├── crawled_data.csv       # CSV output
    ├── page_loaded.png        # Initial screenshot
    └── crawl_complete.png     # Final screenshot
```

## Security Notes

- The crawler only reads data, it does not modify anything
- All data is saved locally in the `crawl_data/` directory
- No data is sent to external servers
- Screenshots may contain sensitive information

## Notes

1. **Ensure frontend is running** before executing the crawler
2. **Close other Chrome instances** to avoid conflicts
3. **Check output files** in `crawl_data/` after completion
4. **Execution time** depends on data volume and system performance

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Verify all prerequisites are met
4. Check that both frontend and backend are running correctly
