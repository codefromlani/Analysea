# app/db/seeds/partners.py

from ..database import SessionLocal
from app.api.models.partner import Partner
from datetime import date

def seed_partners():
    db = SessionLocal()
    try:
        partners_to_seed = [
            {"name": "Global Tech Solutions", "partnership_start_date": date(2022, 5, 10)},
            {"name": "Community Outreach Foundation", "partnership_start_date": date(2021, 11, 25)},
            {"name": "Innovate Education Inc.", "partnership_start_date": date(2023, 2, 1)},
            {"name": "Learning for All", "partnership_start_date": date(2024, 8, 15)},
        ]

        for data in partners_to_seed:
            existing_partner = db.query(Partner).filter(Partner.name == data["name"]).first()
            if not existing_partner:
                db_partner = Partner(**data)
                db.add(db_partner)
                print(f"Adding partner: {data['name']}")

        db.commit()
        print("✅ Partners table seeded successfully.")
    finally:
        db.close()