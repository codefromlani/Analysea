# app/db/seeds/learners.py

from ..database import SessionLocal
from app.api.models.learner import Learner
from datetime import date

def seed_learners():
    db = SessionLocal()
    try:
        learners_to_seed = [
            # Cohort Jan-Mar, Program 1
            {"name": "John Doe", "age": 25, "enrollment_date": date(2023, 1, 15), "program_id": 1, "is_completed": True},
            {"name": "Jane Smith", "age": 30, "enrollment_date": date(2023, 2, 20), "program_id": 1, "is_completed": True},
            {"name": "Chris Green", "age": 29, "enrollment_date": date(2023, 3, 10), "program_id": 1, "is_completed": False},
            {"name": "Jessica Lee", "age": 24, "enrollment_date": date(2023, 3, 25), "program_id": 1, "is_completed": True},

            # Cohort Apr-Jun, Program 2
            {"name": "Michael Brown", "age": 22, "enrollment_date": date(2023, 4, 5), "program_id": 2, "is_completed": True},
            {"name": "Emily White", "age": 28, "enrollment_date": date(2023, 5, 15), "program_id": 2, "is_completed": False},
            {"name": "David Black", "age": 26, "enrollment_date": date(2023, 6, 10), "program_id": 2, "is_completed": True},

            # Cohort Jul-Sep, Program 1
            {"name": "Anna Blue", "age": 23, "enrollment_date": date(2023, 7, 12), "program_id": 1, "is_completed": False},
            {"name": "Tom Gray", "age": 27, "enrollment_date": date(2023, 8, 18), "program_id": 1, "is_completed": True},

            # Cohort Oct-Dec, Program 3
            {"name": "Linda Red", "age": 31, "enrollment_date": date(2023, 10, 2), "program_id": 3, "is_completed": True},
            {"name": "Steve Yellow", "age": 29, "enrollment_date": date(2023, 11, 20), "program_id": 3, "is_completed": False},
        ]

        for data in learners_to_seed:
            existing_learner = db.query(Learner).filter(Learner.name == data["name"]).first()
            if not existing_learner:
                db_learner = Learner(**data)
                db.add(db_learner)
                print(f"Adding Learner: {data['name']}")

        db.commit()
        print("✅ Learners table seeded successfully.")
    finally:
        db.close()
