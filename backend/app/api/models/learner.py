# app/api/models/learner.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Learner(Base):
    __tablename__ = "learners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, nullable=False)
    enrollment_date = Column(Date)
    program_id = Column(Integer, ForeignKey("programs.id"))
    is_completed = Column(Boolean, default=False)
    
    program = relationship("Program", back_populates="learners")