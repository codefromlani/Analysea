from pydantic import BaseModel
from datetime import date

class VolunteerHoursBase(BaseModel):
    volunteer_id: int
    hours_contributed: float
    date_contributed: date

class VolunteerHoursCreate(VolunteerHoursBase):
    pass

class VolunteerHours(VolunteerHoursBase):
    id: int

    class Config:
        from_attributes = True