# app/api/services/impact.py

from sqlalchemy.orm import Session
from typing import List, Dict
from sqlalchemy import extract, func

from ..models.learner import Learner
from ..models.program_cohort import ProgramCohort
from ..models.enrollment import Enrollment
from ..models.course import Course

class ImpactService:
    def __init__(self, db: Session):
        self.db = db

    def get_learner_impact_trend(self, program_id: int, year: int = None) -> List[Dict]:
        """Calculates the completion percentage for each program cohort."""
        cohorts = self.db.query(ProgramCohort).filter(
            ProgramCohort.program_id == program_id
        ).order_by(ProgramCohort.start_date).all()

        results = []

        for cohort in cohorts:
            enrolled_query = self.db.query(Learner).filter(
                Learner.enrollment_date >= cohort.start_date,
                Learner.enrollment_date <= cohort.end_date,
                Learner.program_id == program_id
            )

            if year:
                enrolled_query = enrolled_query.filter(extract('year', Learner.enrollment_date) == year)

            completed_query = enrolled_query.filter(Learner.is_completed == True)

            enrolled = enrolled_query.count()
            completed = completed_query.count()

            percentage = round((completed / enrolled) * 100, 2) if enrolled > 0 else 0

            results.append({
                "cohort": cohort.name,
                "percentage": percentage
            })

        return results

    def get_learner_demographics_by_age(self, year: int = None, program_id: int = None) -> Dict:
            """Calculates the age distribution of all learners."""
            query = self.db.query(Learner)

            if year:
                query = query.filter(extract('year', Learner.enrollment_date) == year)
            if program_id:
                query = query.filter(Learner.program_id == program_id)

            total_learners = query.count()

            if total_learners == 0:
                return {
                    "total_beneficiaries": 0,
                    "demographics": []
                }

            count_18_25 = query.filter(Learner.age.between(18, 25)).count()
            count_26_35 = query.filter(Learner.age.between(26, 35)).count()
            count_36_40 = query.filter(Learner.age.between(36, 40)).count()

            percent_18_25 = round((count_18_25 / total_learners) * 100, 2)
            percent_26_35 = round((count_26_35 / total_learners) * 100, 2)
            percent_36_40 = round((count_36_40 / total_learners) * 100, 2)

            return {
                "total_beneficiaries": total_learners,
                "demographics": [
                    {"age_range": "18 - 25", "percentage": percent_18_25},
                    {"age_range": "26 - 35", "percentage": percent_26_35},
                    {"age_range": "36 - 40", "percentage": percent_36_40}
                ]
            }

    def get_course_learner_distribution(self, year: int = None, program_id: int = None) -> Dict:
        """Calculates the percentage of learners enrolled in each course."""

        query = self.db.query(Learner).join(Enrollment).join(Course)

        if year:
            query = query.filter(extract("year", Learner.enrollment_date) == year)
        if program_id:
            query = query.filter(Learner.program_id == program_id)

        total_learners = query.count()

        if total_learners == 0:
            return {"distribution": []}

        course_counts = (
            self.db.query(
                Course.name,
                func.count(Learner.id).label("learner_count")
            )
            .join(Enrollment, Enrollment.course_id == Course.id)
            .join(Learner, Learner.id == Enrollment.learner_id)
            .filter(
                extract("year", Learner.enrollment_date) == year if year else True,
                Learner.program_id == program_id if program_id else True
            )
            .group_by(Course.name)
            .all()
        )

        distribution = [
            {
                "course": course_name,
                "percentage": round((count / total_learners) * 100, 2),
            }
            for course_name, count in course_counts
        ]

        distribution.sort(key=lambda x: x["percentage"], reverse=True)

        return {"distribution": distribution}

