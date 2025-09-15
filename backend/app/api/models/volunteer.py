# app/api/models/volunteer.py

from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    last_active_date = Column(Date)
    
    hours_log = relationship("VolunteerHours", back_populates="volunteer")
