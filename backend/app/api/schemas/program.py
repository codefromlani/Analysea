# app/api/schemas/program.py

from pydantic import BaseModel

class ProgramSchema(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
