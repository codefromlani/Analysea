# app/db/seeds/learners.py

from ..database import SessionLocal
from app.api.models.learner import Learner
from datetime import date

def seed_learners():
    db = SessionLocal()
    try:
        learners_to_seed = [
            {
                "name": "John Doe",
                "age": 25,
                "enrollment_date": date(2023, 1, 15),
                "program_id": 1 
            },
            {
                "name": "Jane Smith",
                "age": 30,
                "enrollment_date": date(2023, 1, 20),
                "program_id": 1
            },
            {
                "name": "Michael Brown",
                "age": 22,
                "enrollment_date": date(2023, 3, 5),
                "program_id": 2
            },
            {
                "name": "Emily White",
                "age": 28,
                "enrollment_date": date(2023, 4, 10),
                "program_id": 3
            },
            {
                "name": "Chris Green",
                "age": 29,
                "enrollment_date": date(2023, 1, 25),
                "program_id": 1
            },
            {
                "name": "Jessica Lee",
                "age": 24,
                "enrollment_date": date(2023, 1, 10),
                "program_id": 1
            }
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
