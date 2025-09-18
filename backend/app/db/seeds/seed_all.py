# app/db/seeds/seed_all.py

from app.db.seeds import (
    seed_partners,
    seed_programs,
    seed_learners,
    seed_volunteers,
    seed_volunteer_hours,
    seed_program_cohorts,
    seed_courses,
    seed_enrollments,
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

    print("🌱 Seeding Program Cohorts Hours...")
    seed_program_cohorts()

    print("🌱 Seeding Courses...")
    seed_courses()

    print("🌱 Seeding Enrollments...")
    seed_enrollments()

    print("✅ All seeders completed successfully!")

if __name__ == "__main__":
    run()

# python -m app.db.seeds.seed_all