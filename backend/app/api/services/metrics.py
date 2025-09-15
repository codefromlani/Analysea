from sqlalchemy.orm import Session
from ..models.learner import Learner
from ..models.partner import Partner
from ..models.volunteer import Volunteer
from ..models.volunteer_hours import VolunteerHours
from sqlalchemy import func
from sqlalchemy import extract


class MetricService:
    def __init__(self, db: Session):
        self.db = db

    def get_total_learners(self, year: int = None, program_id: int = None) -> int:
        """Returns the total count of all learners."""
        query = self.db.query(Learner)
        if year:
            query = query.filter(extract('year', Learner.enrollment_date) == year)
        if program_id:
            query = query.filter(Learner.program_id == program_id)
        return query.count()

    def get_total_partners(self) -> int:
        """Returns the total count of all support partners."""
        return self.db.query(Partner).count()

    def get_total_volunteer_hours(self, year: int = None, program_id: int = None) -> float:
        """Returns the total hours contributed by all volunteers."""
        query = self.db.query(func.sum(VolunteerHours.hours_contributed))
        if year:
            query = query.filter(extract("year", VolunteerHours.date_contributed) == year)
        if program_id:
            query = query.filter(VolunteerHours.program_id == program_id)
        total_hours = query.scalar()
        return total_hours or 0.0

    def get_total_active_volunteers(self, year: int = None, program_id: int = None) -> int:
        """Returns the count of active volunteers."""
        query = self.db.query(Volunteer).filter(Volunteer.is_active == True)

        if year or program_id:
            query = query.join(Volunteer.hours_log)

            if year:
                query = query.filter(extract("year", VolunteerHours.date_contributed) == year)
            if program_id:
                query = query.filter(VolunteerHours.program_id == program_id)

            query = query.distinct(Volunteer.id)

        return query.count()