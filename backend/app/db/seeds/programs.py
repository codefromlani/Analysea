# app/db/seeds/programs.py

from ..database import SessionLocal
from app.api.models.program import Program

def seed_programs():
    db = SessionLocal()
    try:
        programs_to_seed = [
            {
                "name": "SCA Academy",
                "description": "Comprehensive program for software development."
            },
            {
                "name": "Data Science Bootcamp",
                "description": "An intensive bootcamp covering data analysis and machine learning."
            },
            {
                "name": "Web Design Fundamentals",
                "description": "Foundational course on HTML, CSS, and JavaScript."
            }
        ]

        for data in programs_to_seed:
            existing_program = db.query(Program).filter(Program.name == data["name"]).first()
            if not existing_program:
                db_program = Program(**data) 
                db.add(db_program)
                print(f"Adding Program: {data['name']}")

        db.commit()
        print("✅ Programs table seeded successfully.")
    finally:
        db.close()
