# app/db/seeds/enrollments.py

from ..database import SessionLocal
from app.api.models.enrollment import Enrollment
from app.api.models.learner import Learner
from app.api.models.course import Course

def seed_enrollments():
    db = SessionLocal()
    try:
        courses = {c.name: c for c in db.query(Course).filter(Course.program_id == 1).all()}
        if not courses:
            print("⚠️ No courses found. Run seed_courses first.")
            return

        cohort_course_map = {
            "Q1": courses.get("Cybersecurity"),
            "Q2": courses.get("Software Engineering"),
            "Q3": courses.get("Product Design"),
            "Q4": courses.get("AI/ML Engineering"),
        }

        learners = db.query(Learner).filter(Learner.program_id == 1).all()
        for learner in learners:
            month = learner.enrollment_date.month
            if 1 <= month <= 3:
                course = cohort_course_map["Q1"]
            elif 4 <= month <= 6:
                course = cohort_course_map["Q2"]
            elif 7 <= month <= 9:
                course = cohort_course_map["Q3"]
            else:
                course = cohort_course_map["Q4"]

            if not course:
                continue

            existing_enrollment = db.query(Enrollment).filter(
                Enrollment.learner_id == learner.id,
                Enrollment.course_id == course.id
            ).first()

            if not existing_enrollment:
                enrollment = Enrollment(
                    learner_id=learner.id,
                    course_id=course.id,
                    program_id=1
                )
                db.add(enrollment)
                print(f"Enrolling {learner.name} ({learner.enrollment_date}) in {course.name}")

        db.commit()
        print("✅ Enrollments table seeded successfully.")
    finally:
        db.close()
