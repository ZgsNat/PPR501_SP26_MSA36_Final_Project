# dirty_seed.py
import random
from faker import Faker
import sys
import os

# Cho phép import src/*
sys.path.append(os.getcwd())

from src.infrastructure.db.database import SessionLocal, Base, engine
from src.adapters.repositories.sqlalchemy_student_repository import StudentORM

# Ensure tables exist
Base.metadata.create_all(bind=engine)

TOTAL_RECORDS = 400
fake = Faker("vi_VN")


# ================= DIRTY GENERATORS ================= #

def get_dirty_score():
    """
    Dirty về GIÁ TRỊ nhưng luôn đúng KIỂU float / None
    """
    chance = random.random()

    if chance < 0.1:
        return None                 # mất dữ liệu
    if chance < 0.15:
        return -round(random.uniform(0, 5), 2)   # điểm âm
    if chance < 0.2:
        return round(random.uniform(11, 20), 2)  # nhập nhầm hệ 20
    if chance < 0.23:
        return 100.0               # điểm lố
    return round(random.uniform(0, 10), 4)


def get_dirty_hometown():
    provinces = ["Hà Nội", "Hải Phòng", "Đà Nẵng", "TP HCM", "Cần Thơ"]
    base = random.choice(provinces)
    chance = random.random()

    if chance < 0.1:
        return None
    if chance < 0.18:
        return base.lower()
    if chance < 0.25:
        return base.upper()
    if chance < 0.32:
        return f" {base} "
    if chance < 0.4:
        return "HN"
    if chance < 0.48:
        return "HCM"
    if chance < 0.55:
        return "Ho Chi Minh City"
    if chance < 0.6:
        return "Ha Nioj"
    return base


def get_dirty_email():
    chance = random.random()
    email = fake.email()

    if chance < 0.1:
        return None
    if chance < 0.18:
        return email.replace("@", "")
    if chance < 0.25:
        return email.upper()
    if chance < 0.32:
        return email.replace(".com", "")
    if chance < 0.38:
        return f" {email} "
    return email


def get_dirty_phone():
    chance = random.random()
    phone = fake.phone_number()

    if chance < 0.1:
        return None
    if chance < 0.18:
        return phone[:5]
    if chance < 0.25:
        return phone + "abc"
    if chance < 0.32:
        return phone.replace("0", "")
    return phone


def get_dirty_birth_date():
    chance = random.random()
    date = fake.date_of_birth(minimum_age=18, maximum_age=23)

    if chance < 0.1:
        return None
    if chance < 0.18:
        return date.strftime("%Y-%m-%d")   # sai format
    if chance < 0.25:
        return "32/13/2002"
    if chance < 0.3:
        return "unknown"
    return date.strftime("%d/%m/%Y")


# ================= SEED ================= #

def seed_data():
    db = SessionLocal()
    try:
        if db.query(StudentORM).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        print(f"Initializing {TOTAL_RECORDS} dirty students...")
        students = []

        for i in range(TOTAL_RECORDS):
            student = StudentORM(
                student_id=f"SV{1000 + i}",
                full_name=fake.name(),
                email=get_dirty_email(),
                phone=get_dirty_phone(),
                birth_date=get_dirty_birth_date(),
                home_town=get_dirty_hometown(),
                math_score=get_dirty_score(),
                literature_score=get_dirty_score(),
                english_score=get_dirty_score(),
            )
            students.append(student)

        db.add_all(students)
        db.commit()
        print(" Successfully seeded dirty data (type-safe).")

    except Exception as e:
        print(" Error seeding data:", e)
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
