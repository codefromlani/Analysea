# app/db/seeds/volunteers.py

from ..database import SessionLocal
from app.api.models.volunteer import Volunteer
from datetime import date

def seed_volunteers():
    db = SessionLocal()
    try:
        volunteers_to_seed = [
            {
                "name": "Alex Johnson",
                "is_active": True,
                "last_active_date": date(2023, 8, 20)
            },
            {
                "name": "Sarah Miller",
                "is_active": True,
                "last_active_date": date(2023, 8, 18)
            },
            {
                "name": "David Chen",
                "is_active": False,  
                "last_active_date": date(2022, 12, 10)
            },
            {
                "name": "Laura Williams",
                "is_active": True,
                "last_active_date": date(2023, 8, 22)
            },
            {
                "name": "Robert Davis",
                "is_active": True,
                "last_active_date": date(2023, 8, 15)
            }
        ]

        for data in volunteers_to_seed:
            existing_volunteer = db.query(Volunteer).filter(Volunteer.name == data["name"]).first()
            if not existing_volunteer:
                db_volunteer = Volunteer(**data)
                db.add(db_volunteer)
                print(f"Adding Volunteer: {data['name']}")

        db.commit()
        print("✅ Volunteers table seeded successfully.")
    finally:
        db.close()
