# app/api/models/partner.py

from sqlalchemy import Column, Integer, String, Date
from app.db.database import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    partnership_start_date = Column(Date)