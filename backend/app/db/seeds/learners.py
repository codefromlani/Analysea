# app/db/seeds/learners.py

import random
from ..database import SessionLocal
from app.api.models.learner import Learner
from datetime import date, timedelta

def seed_learners():
    db = SessionLocal()
    try:
        learners_to_seed = []
   
        start_date = date(2025, 1, 1)

        for i in range(1, 51):
            age = random.randint(18, 40)
     
            enrollment_delta = timedelta(days=i * 7.2)
            enrollment_date = start_date + enrollment_delta
       
            is_completed = random.random() < 0.85 

            learners_to_seed.append({
                "name": f"Learner {i}",
                "age": age,
                "enrollment_date": enrollment_date,
                "program_id": 1,
                "is_completed": is_completed
            })

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
