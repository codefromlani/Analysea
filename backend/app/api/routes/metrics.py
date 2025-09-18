from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from ..services.metrics import MetricService
from ..models.program import Program
from ..schemas.program import ProgramSchema

router = APIRouter()

def get_metric_service(db: Session = Depends(get_db)) -> MetricService:
    """Dependency that provides a MetricService instance."""
    return MetricService(db)

@router.get("/metrics/summary")
def read_metrics_summary(
    year: int = Query(None),
    program_id: int = Query(None),
    metrics: MetricService = Depends(get_metric_service)
):
    return {
        "totalLearners": metrics.get_total_learners(year=year, program_id=program_id),
        "supportPartners": metrics.get_total_partners(), 
        "volunteerHours": metrics.get_total_volunteer_hours(year=year, program_id=program_id),
        "activeVolunteers": metrics.get_total_active_volunteers(year=year, program_id=program_id),
    }

@router.get("/programs", response_model=List[ProgramSchema])
def read_total_programs(db: Session = Depends(get_db)):
    total_programs = db.query(Program).all()
    return total_programs