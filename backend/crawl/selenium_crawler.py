"""
Selenium Web Crawler for Student Management System
Crawls data from the frontend application running on localhost:3000
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import json
import time
from datetime import datetime
import os


class StudentDataCrawler:
    """
    Crawler class to extract student data from the web application
    """
    
    def __init__(self, base_url="http://localhost:3000", headless=False, output_dir="crawl_data"):
        """
        Initialize the crawler
        
        Args:
            base_url (str): Base URL of the application
            headless (bool): Run browser in headless mode
            output_dir (str): Directory to save crawled data (default: 'crawl_data')
        """
        self.base_url = base_url
        self.headless = headless
        self.driver = None
        self.output_dir = output_dir
        self.data = {
            'students': [],
            'table_structure': {},
            'metadata': {}
        }
        
        # Create output directory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(script_dir, output_dir)
        os.makedirs(self.output_path, exist_ok=True)
        
    def setup_driver(self):
        """Setup Chrome WebDriver with optimized options for performance"""
        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        # Performance optimizations
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-images')  # Don't load images
        options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
        options.add_argument('--disable-javascript-harmony-shipping')
        options.add_argument('--window-size=1920,1080')
        
        # Disable unnecessary features for speed
        prefs = {
            'profile.managed_default_content_settings.images': 2,  # Disable images
            'profile.default_content_setting_values.notifications': 2,  # Disable notifications
        }
        options.add_experimental_option('prefs', prefs)
        
        # Suppress logging
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)  # Reduced from 10 to 5 seconds
        
        print("✓ WebDriver initialized successfully")
        
    def navigate_to_dashboard(self):
        """Navigate to the student dashboard"""
        try:
            print(f"\n→ Navigating to {self.base_url}...")
            self.driver.get(self.base_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(1)  # Reduced wait time for performance
            
            print(f"✓ Successfully loaded: {self.driver.title}")
            return True
            
        except TimeoutException:
            print("✗ Timeout waiting for page to load")
            return False
    
    def set_rows_per_page(self, rows=100):
        """
        Set the number of rows per page to maximum
        
        Args:
            rows (int): Number of rows to display (default: 100)
        """
        try:
            print(f"\n→ Setting rows per page to {rows}...")
            
            # Wait a bit for the page to fully render
            time.sleep(0.5)  # Reduced wait time for performance
            
            # Try to find and click the rows per page dropdown
            # Common selectors for MUI DataGrid pagination
            dropdown_selectors = [
                "//div[contains(@class, 'MuiTablePagination-select')]",
                "//select[contains(@class, 'MuiTablePagination-select')]",
                "//*[@aria-label='Rows per page']",
                "//div[contains(@class, 'MuiSelect-select')]",
            ]
            
            dropdown = None
            for selector in dropdown_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        dropdown = elements[0]
                        print(f"  Found dropdown using selector: {selector}")
                        break
                except:
                    continue
            
            if not dropdown:
                print("  ⚠ Rows per page dropdown not found, continuing with default...")
                return False
            
            # Click the dropdown to open options
            dropdown.click()
            time.sleep(0.5)  # Reduced wait time
            
            # Try to find and click the option for maximum rows
            option_selectors = [
                f"//li[@data-value='{rows}']",
                f"//option[@value='{rows}']",
                f"//*[contains(text(), '{rows}')]",
                "//li[last()]",  # Last option is usually the maximum
            ]
            
            option_clicked = False
            for selector in option_selectors:
                try:
                    options = self.driver.find_elements(By.XPATH, selector)
                    if options:
                        options[0].click()
                        option_clicked = True
                        print(f"  Selected {rows} rows per page")
                        break
                except:
                    continue
            
            if not option_clicked:
                print("  ⚠ Could not select rows per page option")
                return False
            
            # Wait for table to reload with new pagination
            time.sleep(1.5)  # Reduced wait time
            
            print(f"✓ Successfully set to {rows} rows per page")
            return True
            
        except Exception as e:
            print(f"  ⚠ Error setting rows per page: {e}")
            return False
            
    def extract_table_structure(self):
        """Extract table headers and structure"""
        try:
            print("\n→ Extracting table structure...")
            
            # Try multiple selectors for table headers
            header_selectors = [
                "//table//thead//th",
                "//table//tr[1]//th",
                "//div[contains(@class, 'MuiDataGrid')]//div[contains(@class, 'columnHeader')]",
                "//th",
            ]
            
            headers = []
            for selector in header_selectors:
                try:
                    header_elements = self.driver.find_elements(By.XPATH, selector)
                    if header_elements:
                        headers = [elem.text.strip() for elem in header_elements if elem.text.strip()]
                        if headers:
                            print(f"  Found {len(headers)} columns using selector: {selector}")
                            break
                except:
                    continue
            
            if not headers:
                print("  ⚠ No table headers found, attempting to extract from data rows...")
                # Try to infer from data attributes or other sources
                headers = self._infer_headers_from_data()
            
            self.data['table_structure'] = {
                'columns': headers,
                'column_count': len(headers),
                'extracted_at': datetime.now().isoformat()
            }
            
            print(f"✓ Table structure extracted: {headers}")
            return headers
            
        except Exception as e:
            print(f"✗ Error extracting table structure: {e}")
            return []
    
    def _infer_headers_from_data(self):
        """Infer column headers from data attributes or other sources"""
        try:
            # Try to find data-field attributes (common in MUI DataGrid)
            columns = self.driver.find_elements(By.XPATH, "//*[@data-field]")
            if columns:
                headers = [col.get_attribute('data-field') for col in columns[:10]]  # Limit to reasonable number
                return list(dict.fromkeys(headers))  # Remove duplicates while preserving order
        except:
            pass
        
        return ['ID', 'Name', 'Email', 'Major', 'GPA', 'Status']  # Default fallback
    
    def extract_student_data(self):
        """Extract all student data from the table"""
        try:
            print("\n→ Extracting student data...")
            
            # Wait for table to be present
            time.sleep(1)  # Reduced wait time
            
            # Try multiple strategies to find table rows
            row_selectors = [
                "//table//tbody//tr",
                "//div[contains(@class, 'MuiDataGrid-row')]",
                "//tr[contains(@class, 'student')]",
                "//tbody//tr",
            ]
            
            rows = []
            for selector in row_selectors:
                try:
                    row_elements = self.driver.find_elements(By.XPATH, selector)
                    if row_elements and len(row_elements) > 0:
                        rows = row_elements
                        print(f"  Found {len(rows)} rows using selector: {selector}")
                        break
                except:
                    continue
            
            if not rows:
                print("  ⚠ No data rows found in table")
                return []
            
            students = []
            headers = self.data['table_structure'].get('columns', [])
            
            for idx, row in enumerate(rows, 1):
                try:
                    # Extract cells from row
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    if not cells:
                        # Try alternative cell selector for MUI DataGrid
                        cells = row.find_elements(By.XPATH, ".//div[contains(@class, 'MuiDataGrid-cell')]")
                    
                    if cells:
                        cell_data = [cell.text.strip() for cell in cells]
                        
                        # Create student record
                        if headers and len(cell_data) == len(headers):
                            student = dict(zip(headers, cell_data))
                        else:
                            # Fallback: create numbered columns
                            student = {f'column_{i+1}': value for i, value in enumerate(cell_data)}
                        
                        students.append(student)
                        
                        if idx % 10 == 0:
                            print(f"  Processed {idx} rows...")
                            
                except Exception as e:
                    print(f"  ⚠ Error processing row {idx}: {e}")
                    continue
            
            self.data['students'] = students
            print(f"✓ Extracted {len(students)} student records")
            return students
            
        except Exception as e:
            print(f"✗ Error extracting student data: {e}")
            return []
    
    def crawl_all_pages(self):
        """
        Crawl data from all pagination pages
        Returns total number of records crawled
        """
        try:
            print("\n→ Crawling all pages...")
            
            all_students = []
            current_page = 1
            
            # Extract first page
            students_on_page = self.extract_student_data()
            all_students.extend(students_on_page)
            
            # Check if there are more pages
            total_records = self.get_total_records()
            rows_per_page = len(students_on_page)
            
            if total_records and rows_per_page > 0:
                total_pages = (total_records + rows_per_page - 1) // rows_per_page
                print(f"  Total records: {total_records}, Pages: {total_pages}")
                
                # Crawl remaining pages
                while current_page < total_pages:
                    current_page += 1
                    print(f"\n  → Moving to page {current_page}/{total_pages}...")
                    
                    if self.go_to_next_page():
                        time.sleep(1)  # Wait for page to load
                        students_on_page = self.extract_student_data()
                        all_students.extend(students_on_page)
                    else:
                        print(f"  ⚠ Could not navigate to page {current_page}")
                        break
            
            # Update data with all students
            self.data['students'] = all_students
            print(f"\n✓ Total crawled: {len(all_students)} records from {current_page} page(s)")
            return all_students
            
        except Exception as e:
            print(f"✗ Error crawling all pages: {e}")
            return self.data['students']
    
    def get_total_records(self):
        """Get total number of records from pagination info"""
        try:
            # Try to find pagination text like "1–100 of 400"
            pagination_selectors = [
                "//p[contains(@class, 'MuiTablePagination-displayedRows')]",
                "//*[contains(text(), 'of')]",
            ]
            
            for selector in pagination_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        text = elements[0].text
                        # Extract total from "1–100 of 400" format
                        if 'of' in text:
                            parts = text.split('of')
                            if len(parts) == 2:
                                total = int(parts[1].strip().replace(',', ''))
                                return total
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"  ⚠ Could not get total records: {e}")
            return None
    
    def go_to_next_page(self):
        """Click the next page button"""
        try:
            # Try to find and click next button
            next_button_selectors = [
                "//button[@aria-label='Go to next page']",
                "//button[contains(@class, 'MuiTablePagination-actions')]//button[last()]",
                "//*[@data-testid='KeyboardArrowRightIcon']/parent::button",
            ]
            
            for selector in next_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.XPATH, selector)
                    if buttons:
                        button = buttons[0]
                        # Check if button is enabled
                        if not button.get_attribute('disabled'):
                            button.click()
                            return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"  ⚠ Error clicking next page: {e}")
            return False
    
    def extract_page_metadata(self):
        """Extract metadata about the page"""
        try:
            print("\n→ Extracting page metadata...")
            
            metadata = {
                'page_title': self.driver.title,
                'url': self.driver.current_url,
                'crawled_at': datetime.now().isoformat(),
                'total_records': len(self.data['students']),
            }
            
            # Try to find pagination info
            try:
                pagination_elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'of') or contains(text(), 'total') or contains(text(), 'Showing')]")
                if pagination_elements:
                    metadata['pagination_info'] = pagination_elements[0].text
            except:
                pass
            
            # Try to find filter/search elements
            try:
                search_box = self.driver.find_element(By.XPATH, "//input[@type='search' or @placeholder]")
                if search_box:
                    metadata['has_search'] = True
                    metadata['search_placeholder'] = search_box.get_attribute('placeholder')
            except:
                metadata['has_search'] = False
            
            self.data['metadata'] = metadata
            print(f"✓ Metadata extracted: {metadata}")
            return metadata
            
        except Exception as e:
            print(f"✗ Error extracting metadata: {e}")
            return {}
    
    def save_to_json(self, filename='crawled_data.json'):
        """Save crawled data to JSON file"""
        try:
            filepath = os.path.join(self.output_path, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Data saved to JSON: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error saving to JSON: {e}")
            return None
    
    def save_to_excel(self, filename='crawled_data.xlsx'):
        """Save student data to Excel file"""
        try:
            if not self.data['students']:
                print("⚠ No student data to save to Excel")
                return None
            
            filepath = os.path.join(self.output_path, filename)
            
            df = pd.DataFrame(self.data['students'])
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Write student data
                df.to_excel(writer, sheet_name='Students', index=False)
                
                # Write metadata
                metadata_df = pd.DataFrame([self.data['metadata']])
                metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
                
                # Write table structure
                structure_df = pd.DataFrame([self.data['table_structure']])
                structure_df.to_excel(writer, sheet_name='Table Structure', index=False)
            
            print(f"✓ Data saved to Excel: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error saving to Excel: {e}")
            return None
    
    def save_to_csv(self, filename='crawled_data.csv'):
        """Save student data to CSV file"""
        try:
            if not self.data['students']:
                print("⚠ No student data to save to CSV")
                return None
            
            filepath = os.path.join(self.output_path, filename)
            
            df = pd.DataFrame(self.data['students'])
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            print(f"✓ Data saved to CSV: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error saving to CSV: {e}")
            return None
    
    def take_screenshot(self, filename='screenshot.png'):
        """Take a screenshot of the current page"""
        try:
            filepath = os.path.join(self.output_path, filename)
            
            self.driver.save_screenshot(filepath)
            print(f"✓ Screenshot saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error taking screenshot: {e}")
            return None
    
    def crawl(self, save_formats=['json', 'excel', 'csv']):
        """
        Main crawling method
        
        Args:
            save_formats (list): List of formats to save data ('json', 'excel', 'csv')
        """
        try:
            print("=" * 60)
            print("  Student Management System - Web Crawler")
            print("=" * 60)
            
            # Setup
            self.setup_driver()
            
            # Navigate
            if not self.navigate_to_dashboard():
                print("\n✗ Failed to navigate to dashboard")
                return False
            
            # Take initial screenshot
            self.take_screenshot('page_loaded.png')
            
            # Set rows per page to maximum (100)
            self.set_rows_per_page(100)
            
            # Extract data from all pages
            self.extract_table_structure()
            self.crawl_all_pages()  # Changed from extract_student_data()
            self.extract_page_metadata()
            
            # Save data
            print("\n" + "=" * 60)
            print("  Saving Data")
            print("=" * 60)
            
            if 'json' in save_formats:
                self.save_to_json()
            
            if 'excel' in save_formats:
                self.save_to_excel()
            
            if 'csv' in save_formats:
                self.save_to_csv()
            
            # Final screenshot
            self.take_screenshot('crawl_complete.png')
            
            # Summary
            print("\n" + "=" * 60)
            print("  Crawl Summary")
            print("=" * 60)
            print(f"  Total records crawled: {len(self.data['students'])}")
            print(f"  Columns found: {len(self.data['table_structure'].get('columns', []))}")
            print(f"  Page title: {self.data['metadata'].get('page_title', 'N/A')}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n✗ Crawling failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            if self.driver:
                print("\n→ Closing browser...")
                self.driver.quit()
                print("✓ Browser closed")
    
    def get_data(self):
        """Return the crawled data"""
        return self.data


def main():
    """Main execution function"""
    # Create crawler instance
    crawler = StudentDataCrawler(
        base_url="http://localhost:3000",
        headless=False  # Set to True to run without GUI
    )
    
    # Run the crawler
    success = crawler.crawl(save_formats=['json', 'excel', 'csv'])
    
    if success:
        print("\n✓ Crawling completed successfully!")
    else:
        print("\n✗ Crawling failed!")
    
    return crawler.get_data()


if __name__ == "__main__":
    main()
