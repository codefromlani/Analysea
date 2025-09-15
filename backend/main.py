# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.api.routes.metrics import router as metrics_router

import app.api.models  


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

app.include_router(metrics_router, prefix="/api", tags=["metrics"])