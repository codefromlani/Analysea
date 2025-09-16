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
def read_learner_impact_trend(program_id: int, metrics: ImpactService = Depends(get_impact_service)):
    trend_data = metrics.get_learner_impact_trend(program_id=program_id)
    return trend_data