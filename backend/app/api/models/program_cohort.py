# app/api/models/program_cohort.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ProgramCohort(Base):
    __tablename__ = "program_cohorts"
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    name = Column(String)  # e.g., "Jan-Mar"

    program = relationship("Program", back_populates="cohorts")