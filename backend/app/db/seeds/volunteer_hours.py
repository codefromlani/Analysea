# app/db/seeds/volunteer_hours.py

from ..database import SessionLocal
from app.api.models.volunteer_hours import VolunteerHours
from datetime import date

def seed_volunteer_hours():
    db = SessionLocal()
    try:
        volunteer_hours_seed_data = [
            {
                "volunteer_id": 1,  
                "program_id": 1,  
                "hours_contributed": 3.0,
                "date_contributed": date(2023, 8, 17)
            },
            {
                "volunteer_id": 1,  
                "program_id": 1,  
                "hours_contributed": 3.0,
                "date_contributed": date(2023, 8, 20)
            },
            {
                "volunteer_id": 2,  
                "program_id": 2,  
                "hours_contributed": 4.0,
                "date_contributed": date(2023, 8, 18)
            },
            {
                "volunteer_id": 3,  
                "program_id": 3,  
                "hours_contributed": 1.5,
                "date_contributed": date(2022, 12, 10)
            },
            {
                "volunteer_id": 4,  
                "program_id": 1, 
                "hours_contributed": 5.0,
                "date_contributed": date(2023, 8, 22)
            },
            {
                "volunteer_id": 4,  
                "program_id": 1,  
                "hours_contributed": 1.0,
                "date_contributed": date(2023, 8, 23)
            },
            {
                "volunteer_id": 5,  
                "program_id": 1,  
                "hours_contributed": 2.0,
                "date_contributed": date(2023, 8, 15)
            }
        ]

        for data in volunteer_hours_seed_data:
            existing_record = (
                db.query(VolunteerHours)
                .filter(
                    VolunteerHours.volunteer_id == data["volunteer_id"],
                    VolunteerHours.date_contributed == data["date_contributed"]
                )
                .first()
            )
            if not existing_record:
                db_volunteer_hours = VolunteerHours(**data)
                db.add(db_volunteer_hours)
                print(f"Adding Volunteer Hours: Volunteer {data['volunteer_id']} on {data['date_contributed']}")

        db.commit()
        print("✅ Volunteer Hours table seeded successfully.")
    finally:
        db.close()
