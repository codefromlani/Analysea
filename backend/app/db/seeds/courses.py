# app/db/seeds/courses.py

from ..database import SessionLocal
from app.api.models.course import Course

def seed_courses():
    db = SessionLocal()
    try:
        courses_to_seed = [
            {"name": "Cybersecurity", "description": "Cybersecurity basics", "program_id": 1},
            {"name": "Software Engineering", "description": "Intro to software development", "program_id": 1},
            {"name": "Product Design", "description": "Foundations of product design", "program_id": 1},
            {"name": "AI/ML Engineering", "description": "Machine learning essentials", "program_id": 1},
        ]

        for data in courses_to_seed:
            existing_course = db.query(Course).filter(Course.name == data["name"]).first()
            if not existing_course:
                db_course = Course(**data)
                db.add(db_course)
                print(f"Adding Course: {data['name']}")

        db.commit()
        print("✅ Courses table seeded successfully.")
    finally:
        db.close()
