# app/db/seeds/program_cohorts.py

from ..database import SessionLocal
from app.api.models.program_cohort import ProgramCohort
from datetime import date

def seed_program_cohorts():
    db = SessionLocal()
    try:
        # Define cohorts for each program
        cohorts_to_seed = [
            # Program 1 (SCA Academy)
            {"program_id": 1, "name": "Jan-Mar", "start_date": date(2023, 1, 1), "end_date": date(2023, 3, 31)},
            {"program_id": 1, "name": "Apr-Jun", "start_date": date(2023, 4, 1), "end_date": date(2023, 6, 30)},
            {"program_id": 1, "name": "Jul-Sep", "start_date": date(2023, 7, 1), "end_date": date(2023, 9, 30)},
            {"program_id": 1, "name": "Oct-Dec", "start_date": date(2023, 10, 1), "end_date": date(2023, 12, 31)},

            # Program 2
            {"program_id": 2, "name": "Jan-Mar", "start_date": date(2023, 1, 1), "end_date": date(2023, 3, 31)},
            {"program_id": 2, "name": "Apr-Jun", "start_date": date(2023, 4, 1), "end_date": date(2023, 6, 30)},
            {"program_id": 2, "name": "Jul-Sep", "start_date": date(2023, 7, 1), "end_date": date(2023, 9, 30)},
            {"program_id": 2, "name": "Oct-Dec", "start_date": date(2023, 10, 1), "end_date": date(2023, 12, 31)},

            # Program 3
            {"program_id": 3, "name": "Jan-Mar", "start_date": date(2023, 1, 1), "end_date": date(2023, 3, 31)},
            {"program_id": 3, "name": "Apr-Jun", "start_date": date(2023, 4, 1), "end_date": date(2023, 6, 30)},
            {"program_id": 3, "name": "Jul-Sep", "start_date": date(2023, 7, 1), "end_date": date(2023, 9, 30)},
            {"program_id": 3, "name": "Oct-Dec", "start_date": date(2023, 10, 1), "end_date": date(2023, 12, 31)},
        ]

        for data in cohorts_to_seed:
            existing_cohort = db.query(ProgramCohort).filter(
                ProgramCohort.program_id == data["program_id"],
                ProgramCohort.name == data["name"]
            ).first()
            if not existing_cohort:
                db_cohort = ProgramCohort(**data)
                db.add(db_cohort)
                print(f"Adding Program Cohort: {data['name']} for Program {data['program_id']}")

        db.commit()
        print("✅ ProgramCohorts table seeded successfully.")
    finally:
        db.close()
