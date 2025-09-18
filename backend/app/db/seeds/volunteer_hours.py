# app/db/seeds/volunteer_hours.py

from ..database import SessionLocal
from app.api.models.volunteer_hours import VolunteerHours
from datetime import date

def seed_volunteer_hours():
    db = SessionLocal()
    try:
        volunteer_hours_seed_data = [
            # Volunteer 1 Contributions (Total: 95 hours)
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 4.0, "date_contributed": date(2025, 1, 15)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 2, 20)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 3.0, "date_contributed": date(2025, 3, 10)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 8.0, "date_contributed": date(2025, 4, 5)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 5, 25)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 12.0, "date_contributed": date(2025, 6, 18)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 7.0, "date_contributed": date(2025, 7, 12)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 6.0, "date_contributed": date(2025, 8, 28)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 9, 14)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 15.0, "date_contributed": date(2025, 10, 30)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 11, 8)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 12, 1)},
            {"volunteer_id": 1, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 12, 20)},
            
            # Volunteer 2 Contributions (Total: 80 hours)
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 2.0, "date_contributed": date(2025, 1, 10)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 8.0, "date_contributed": date(2025, 2, 14)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 3, 22)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 4, 18)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 15.0, "date_contributed": date(2025, 5, 12)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 6, 1)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 7.0, "date_contributed": date(2025, 7, 25)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 13.0, "date_contributed": date(2025, 8, 30)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 9, 17)},
            {"volunteer_id": 2, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 10, 15)},

            # Volunteer 3 Contributions (Total: 75 hours)
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 1, 20)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 2, 1)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 12.0, "date_contributed": date(2025, 3, 28)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 8.0, "date_contributed": date(2025, 4, 12)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 7.0, "date_contributed": date(2025, 5, 19)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 13.0, "date_contributed": date(2025, 6, 25)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 7, 1)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 8, 8)},
            {"volunteer_id": 3, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 9, 29)},

            # Volunteer 4 Contributions (Total: 80 hours)
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 1, 5)},
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 2, 28)},
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 15.0, "date_contributed": date(2025, 3, 14)},
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 4, 25)},
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 8.0, "date_contributed": date(2025, 5, 1)},
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 12.0, "date_contributed": date(2025, 6, 10)},
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 7, 30)},
            {"volunteer_id": 4, "program_id": 1, "hours_contributed": 15.0, "date_contributed": date(2025, 8, 20)},

            # Volunteer 5 Contributions (Total: 70 hours)
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 3.0, "date_contributed": date(2025, 1, 30)},
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 7.0, "date_contributed": date(2025, 2, 18)},
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 3, 5)},
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 5.0, "date_contributed": date(2025, 4, 20)},
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 15.0, "date_contributed": date(2025, 5, 15)},
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 8.0, "date_contributed": date(2025, 6, 22)},
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 12.0, "date_contributed": date(2025, 7, 7)},
            {"volunteer_id": 5, "program_id": 1, "hours_contributed": 10.0, "date_contributed": date(2025, 8, 1)},
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
