# seed.py
import random
import unicodedata
from faker import Faker
import sys
import os

# Thêm thư mục hiện tại vào sys.path để Python tìm thấy module 'src'
sys.path.append(os.getcwd())

from src.infrastructure.db.database import SessionLocal, Base, engine
# Import StudentORM từ nơi định nghĩa mới
from src.adapters.repositories.sqlalchemy_student_repository import StudentORM

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    try:
        # Check data exists?
        if db.query(StudentORM).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        print("Initializing 100 students...")
        fake = Faker('vi_VN')
        provinces = ["Hà Nội", "Hải Phòng", "Đà Nẵng", "TP HCM", "Cần Thơ", "Nghệ An", "Thanh Hóa"]
        
        students = []
        for i in range(100):
            full_name = unicodedata.normalize('NFC', fake.name())
            home_town = unicodedata.normalize('NFC', random.choice(provinces))
            
            student = StudentORM(
                student_id=f"SV{1000 + i}",
                full_name=full_name,
                email=fake.email(),
                phone=fake.phone_number(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=23).strftime("%d/%m/%Y"),
                home_town=home_town,
                math_score=round(random.uniform(4.0, 10.0), 1),
                literature_score=round(random.uniform(4.0, 10.0), 1),
                english_score=round(random.uniform(4.0, 10.0), 1)
                # created_at sẽ tự động được điền bởi TimestampMixin
            )
            students.append(student)

        db.add_all(students)
        db.commit()
        print("Successfully added 100 students.")
    
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()