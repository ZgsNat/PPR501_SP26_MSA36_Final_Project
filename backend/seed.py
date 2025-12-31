from app.core.database import SessionLocal, Base, engine
from app.models.student_entity import StudentEntity
from faker import Faker
import random

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Check if data already exists to avoid duplicates
    if db.query(StudentEntity).count() > 0:
        print("Database already contains data. Skipping seed.")
        db.close()
        return

    print("Initializing 100 students...")
    fake = Faker('vi_VN')
    provinces = ["Hà Nội", "Hải Phòng", "Đà Nẵng", "TP HCM", "Cần Thơ", "Nghệ An", "Thanh Hóa"]
    
    students = []
    for i in range(100):
        student = StudentEntity(
            student_id=f"SV{1000 + i}",
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=23).strftime("%d/%m/%Y"),
            home_town=random.choice(provinces),
            math_score=round(random.uniform(4.0, 10.0), 1),
            literature_score=round(random.uniform(4.0, 10.0), 1),
            english_score=round(random.uniform(4.0, 10.0), 1)
        )
        students.append(student)

    db.add_all(students)
    db.commit()
    print("Successfully added 100 students.")
    db.close()

if __name__ == "__main__":
    seed_data()