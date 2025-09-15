# app/api/models/volunteer_hours.py

from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class VolunteerHours(Base):
    __tablename__ = "volunteer_hours"

    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"))
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)
    hours_contributed = Column(Float)
    date_contributed = Column(Date)

    volunteer = relationship("Volunteer", back_populates="hours_log")
    program = relationship("Program", back_populates="volunteer_hours")
