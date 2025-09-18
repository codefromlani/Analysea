# app/api/services/report.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from .metrics import MetricService
from .impact import ImpactService

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class ReportService:
    def __init__(self, db: Session, model_name: str = "gemini-1.5-flash"):
        """Initialize ReportService with DB session + Gemini model."""
        self.db = db
        self.metrics = MetricService(db)
        self.impact = ImpactService(db)
        self.model = genai.GenerativeModel(model_name)

    def get_stats(self, year: int = None, program_id: int = None) -> dict:
        """Fetch stats from MetricService and return as dict."""
        return {
            "total_learners": self.metrics.get_total_learners(year=year, program_id=program_id),
            "support_partners": self.metrics.get_total_partners(),
            "volunteer_hours": self.metrics.get_total_volunteer_hours(year=year, program_id=program_id),
            "active_volunteers": self.metrics.get_total_active_volunteers(year=year, program_id=program_id),
        }

    def summarize_impact(self, data: dict) -> str:
        """Generate donor-friendly summary using Gemini."""
        prompt = f"""
        You are helping an NGO write a donor-friendly impact report.

        Stats provided:
        - Total learners: {data.get('total_learners', 0)}
        - Support partners: {data.get('support_partners', 0)}
        - Volunteer hours: {data.get('volunteer_hours', 0)}
        - Active volunteers: {data.get('active_volunteers', 0)}

        Write a short, positive summary (3–4 sentences) highlighting achievements.
        Make it clear, inspiring, and professional.
        """

        response = self.model.generate_content(prompt)
        return response.text if response and response.text else "No summary generated."

    def generate_report(self, year: int = None, program_id: int = None) -> dict:
        """Fetch all dashboard data and generate a full report."""
        # 1. Stats
        stats = self.get_stats(year=year, program_id=program_id)

        # 2. Executive summary
        summary = self.summarize_impact(stats)

        # --- Step 3: Dashboard data ---
        learner_trend = self.impact.get_learner_impact_trend(program_id, year)
        demographics = self.impact.get_learner_demographics_by_age(year, program_id)
        course_distribution = self.impact.get_course_learner_distribution(year, program_id)

        return {
            "stats": stats,
            "summary": summary,
            "learner_trend": learner_trend,
            "demographics": demographics,
            "course_distribution": course_distribution
        }

 