from pydantic import BaseModel
from datetime import date

class PartnerBase(BaseModel):
    name: str
    partnership_start_date: date

class PartnerCreate(PartnerBase):
    pass

class Partner(PartnerBase):
    id: int

    class Config:
        from_attributes = True