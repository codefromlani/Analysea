from pydantic import BaseModel
from datetime import date

class VolunteerBase(BaseModel):
    name: str
    is_active: bool = True  
    last_active_date: date

class VolunteerCreate(VolunteerBase):
    pass

class Volunteer(VolunteerBase):
    id: int
    total_hours_contributed: float = 0.0  

    class Config:
        from_attributes = True