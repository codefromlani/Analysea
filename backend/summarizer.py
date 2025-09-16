import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# The summarizer function
def summarize_impact(data: dict) -> str:
    """
    Summarize NGO impact stats into a donor-friendly narrative.

    Args:
        data (dict): Example:
            {
                "total_learners": 120,
                "support_partners": 19,
                "volunteer_hours": 85,
                "active_volunteers": 30
            }

    Returns:
        str: AI-generated summary text.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

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

    response = model.generate_content(prompt)

    return response.text if response and response.text else "No summary generated."
