from pydantic import BaseModel
from datetime import date

class LearnerBase(BaseModel):
    name: str
    enrollment_date: date
    academy_name: str

class LearnerCreate(LearnerBase):
    pass

class Learner(LearnerBase):
    id: int

    class Config:
        from_attributes = True