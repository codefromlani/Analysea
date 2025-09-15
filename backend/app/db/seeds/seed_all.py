# app/db/seeds/seed_all.py

from app.db.seeds import (
    seed_partners,
    seed_programs,
    seed_learners,
    seed_volunteers,
    seed_volunteer_hours,
)

def run():
    print("🌱 Seeding Partners...")
    seed_partners()

    print("🌱 Seeding Programs...")
    seed_programs()

    print("🌱 Seeding Learners...")
    seed_learners()

    print("🌱 Seeding Volunteers...")
    seed_volunteers()

    print("🌱 Seeding Volunteer Hours...")
    seed_volunteer_hours()

    print("✅ All seeders completed successfully!")

if __name__ == "__main__":
    run()

# python -m app.db.seeds.seed_all