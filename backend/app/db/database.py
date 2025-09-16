from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# am I supposed to use 'db' or 'base' or what so as to connect with supabase here?
# backend/db.py
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_impact_stats():
    """
    Fetch NGO impact stats from Supabase.
    Expected table: 'impact_stats'
    Example row: { totalLearners, supportPartners, volunteerHours, activeVolunteers }
    """
    response = supabase.table("impact_stats").select("*").execute() # so i can know what to use here ..................

    if response.data and len(response.data) > 0:
        return response.data[0]  # take first row for demo
    return {"learners_reached": 0, "volunteer_hours": 0, "events_hosted": 0}
