from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.api.routes.metrics import router as metrics_router
from app.api.routes.impact import router as impact_router

import app.api.models 

from summarizer import summarize_impact
from db import get_impact_stats  # added this in database.py



# Base.metadata.drop_all(bind=engine)
# print("All tables dropped")

# Recreate tables from models
Base.metadata.create_all(bind=engine)
print("All tables created")

app = FastAPI(title="Analysea API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def health_check():
    return {"message": f"Server is running and healthy"}

# check here .....................
@app.get("/report")
def generate_report():
    # Fetch stats from Supabase
    stats = get_impact_stats()

    # Pass stats to Gemini summarizer
    summary = summarize_impact(stats)

    return {
        "stats": stats,
        "summary": summary
    }

app.include_router(metrics_router, prefix="/api", tags=["metrics"])
app.include_router(impact_router, prefix="/api", tags=["impact"])
