# app/api/routes/impact.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from app.db.database import get_db
from ..services.impact import ImpactService

router = APIRouter()

def get_impact_service(db: Session = Depends(get_db)) -> ImpactService:
    """Dependency that provides a ImpactService instance."""
    return ImpactService(db)

@router.get("/impact/learner_impact_trend", response_model=List[Dict])
def read_learner_impact_trend(
    program_id: int, 
    year: int = None,
    metrics: ImpactService = Depends(get_impact_service)):
    trend_data = metrics.get_learner_impact_trend(program_id=program_id, year=year)
    return trend_data

@router.get("/learner_demographics", response_model=Dict)
def read_learner_demographics(
    year: int = None,
    program_id: int = None,
    metrics: ImpactService = Depends(get_impact_service)
):
    demographics_data = metrics.get_learner_demographics_by_age(year=year, program_id=program_id)
    return demographics_data

@router.get("/learner/course_distribution", response_model=Dict)
def read_course_distribution(
    year: int = None,
    program_id: int = None,
    metrics: ImpactService = Depends(get_impact_service)
):
    distribution_data = metrics.get_course_learner_distribution(year=year, program_id=program_id)
    return distribution_data