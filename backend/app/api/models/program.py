# app/api/models/program.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    learners = relationship("Learner", back_populates="program")
    volunteer_hours = relationship("VolunteerHours", back_populates="program") 
    cohorts = relationship("ProgramCohort", back_populates="program")
    courses = relationship("Course", back_populates="program")
    enrollments = relationship("Enrollment", back_populates="program", cascade="all, delete-orphan")
