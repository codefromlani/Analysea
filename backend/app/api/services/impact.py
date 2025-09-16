# app/api/services/impact.py

from sqlalchemy.orm import Session
from ..models.learner import Learner
from ..models.program_cohort import ProgramCohort
from typing import List, Dict

class ImpactService:
    def __init__(self, db: Session):
        self.db = db

    def get_learner_impact_trend(self, program_id: int) -> List[Dict]:
        """
        Calculates the completion percentage for each program cohort.
        """
        cohorts = self.db.query(ProgramCohort).filter(
            ProgramCohort.program_id == program_id
        ).all()

        results = []

        for cohort in cohorts:
            enrolled = self.db.query(Learner).filter(
                Learner.enrollment_date >= cohort.start_date,
                Learner.enrollment_date <= cohort.end_date
            ).count()

            completed = self.db.query(Learner).filter(
                Learner.enrollment_date >= cohort.start_date,
                Learner.enrollment_date <= cohort.end_date,
                Learner.is_completed == True
            ).count()

            percentage = round((completed / enrolled) * 100, 2) if enrolled > 0 else 0

            results.append({
                "cohort": cohort.name,
                "percentage": percentage
            })

        return results
