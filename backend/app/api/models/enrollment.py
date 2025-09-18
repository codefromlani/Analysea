from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)

    # Define relationships
    learner = relationship("Learner", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    program = relationship("Program", back_populates="enrollments")
