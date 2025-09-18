# app/api/routes/report.py

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, HTMLResponse
from sqlalchemy.orm import Session
from io import BytesIO
from weasyprint import HTML
import matplotlib.pyplot as plt
import base64

from app.db.database import get_db
from ..services.report import ReportService

router = APIRouter()

def get_report_service(db: Session = Depends(get_db)) -> ReportService:
    """Dependency that provides a ReportService instance."""
    return ReportService(db)

@router.get("/report")
def generate_report(
    year: int = Query(None),
    program_id: int = Query(None),
    report: ReportService = Depends(get_report_service)
):
    return report.generate_report(year=year, program_id=program_id)

@router.get("/report/start")
def start_report(
    year: int = Query(...),
    program_id: int = Query(...),
):
    pdf_url = f"/api/report/pdf?year={year}&program_id={program_id}"
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generating Report - ANALYSEA</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #334155;
        }}
        
        .container {{
            text-align: center;
            padding: 2rem;
            max-width: 400px;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #1e293b;
            margin-bottom: 3rem;
            letter-spacing: -0.025em;
        }}
        
        .spinner {{
            width: 48px;
            height: 48px;
            border: 3px solid #e2e8f0;
            border-top: 3px solid #ec4899;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 2rem;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .title {{
            font-size: 1.125rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.5rem;
            line-height: 1.5;
        }}
        
        .subtitle {{
            font-size: 0.875rem;
            color: #64748b;
            line-height: 1.6;
            margin-bottom: 2rem;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 2px;
            background-color: #e2e8f0;
            border-radius: 1px;
            overflow: hidden;
            margin-top: 1rem;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ec4899, #f97316);
            width: 0%;
            border-radius: 1px;
            animation: progress 3s ease-in-out infinite;
        }}
        
        @keyframes progress {{
            0% {{ width: 0%; }}
            50% {{ width: 60%; }}
            100% {{ width: 90%; }}
        }}
        
        .error {{
            color: #dc2626;
            font-size: 0.875rem;
            margin-top: 1rem;
            padding: 0.75rem;
            background-color: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 6px;
            display: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        
        <h1 class="title">Generating Your Report</h1>
        <p class="subtitle">Please wait while we compile your impact data and insights...</p>
        
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        
        <div id="error" class="error"></div>
    </div>

    <script>
        async function fetchPdf() {{
            try {{
                const res = await fetch("{pdf_url}");
                if (!res.ok) {{
                    throw new Error(`HTTP ${{res.status}}: ${{res.statusText}}`);
                }}
                window.location.href = "{pdf_url}";
            }} catch (err) {{
                const errorDiv = document.getElementById('error');
                errorDiv.textContent = `Failed to generate report: ${{err.message}}`;
                errorDiv.style.display = 'block';
                
                // Hide spinner and progress bar
                document.querySelector('.spinner').style.display = 'none';
                document.querySelector('.progress-bar').style.display = 'none';
                
                // Update title
                document.querySelector('.title').textContent = 'Report Generation Failed';
                document.querySelector('.subtitle').textContent = 'Please try again or contact support if the issue persists.';
            }}
        }}
        fetchPdf();
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)


@router.get("/report/pdf")
def generate_pdf_report(
    year: int = Query(None),
    program_id: int = Query(None),
    report: ReportService = Depends(get_report_service)
):
    """Return the full report as a PDF."""

    from ..models.program import Program

    data = report.generate_report(year=year, program_id=program_id)

    # --- Learner Impact Trend Chart ---
    trend = data["learner_trend"]
    plt.figure(figsize=(6,3))
    cohorts = [t["cohort"] for t in trend]
    percentages = [t["percentage"] for t in trend]
    plt.bar(cohorts, percentages, color="#ec4899")
    plt.xlabel("Cohort")
    plt.ylabel("Completion %")
    plt.title("Learner Impact Trend")
    plt.ylim(0,100)
    plt.tight_layout()

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches='tight')
    plt.close()
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.read()).decode()

    # --- Course Learner Distribution Narrative ---
    dist = data["course_distribution"]["distribution"]
    if dist:
        dist_text = "Learners are distributed as follows: "
        dist_text += ", ".join([f"{d['course']} ({d['percentage']}%)" for d in dist]) + "."
    else:
        dist_text = "No course enrollment data available."

      # --- Step 5: Program Details (LLM-generated) ---
    program_name = "Unknown Program"
    program_description = "No description available."
    if program_id:
        program_obj = report.db.query(Program).filter(Program.id == program_id).first()
        if program_obj:
            program_name = program_obj.name
            program_description = program_obj.description or program_description

        program_prompt = f"""
    Generate a **short, concise, donor-friendly program summary** for a PDF report (3–4 sentences).

    Program Name: {program_name}
    Goal/Objective: {program_description}
    Outcomes/Impact: {dist_text}

    Include a brief 'Donor Impact / Contribution' statement explaining how donors' support helped this program succeed.
    """
        
        # --- Step 6: Future Plans (LLM) ---
        trend = data["learner_trend"]
        if trend:
            trend_summary = ", ".join([f"{t['cohort']}: {t['percentage']}%" for t in trend])
        else:
            trend_summary = "No learner impact trend data available."

    future_prompt = f"""
    Based on the following program data, generate a **brief donor-friendly future plans** for the next year (3-4 sentences max):

    Program Name: {program_name}
    Key Metrics: Total Learners={data['stats']['total_learners']}, Support Partners={data['stats']['support_partners']}, Volunteer Hours={data['stats']['volunteer_hours']}, Active Volunteers={data['stats']['active_volunteers']}
    Learner Impact Trend: {trend_summary}  
    Course Distribution: {dist_text}

    Provide concise, actionable future plans for the program to maximize its impact in the next year.
    """

    future_plans = report.model.generate_content(future_prompt)
    future_text = future_plans.text if future_plans and future_plans.text else "No future plans generated."



    program_details_result = report.model.generate_content(program_prompt)
    program_details_text = (
        program_details_result.text
        if program_details_result and program_details_result.text
        else "No program details generated."
    )

    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Impact Report {year} - ANALYSEA</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background: #ffffff;
        }}
        
        .page {{
            max-width: 800px;
            margin: 0 auto;
            padding: 1.5rem 2rem;
        }}
        
        /* Cover Page */
        .cover {{
            text-align: center;
            margin-bottom: 1.5rem;
        }}
        
        
        .cover h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }}
        
        .cover .year {{
            display: inline-block;
            background: linear-gradient(135deg, #ec4899, #f97316);
            color: white;
            padding: 0.5rem 1.5rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1rem;
        }}
        
        /* Section Headers */
        h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #ec4899;
            margin: 6rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #fce7f3;
        }}
        
        /* Content Sections */
        .summary {{
            background: #f8fafc;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-size: 1rem;
            page-break-inside: avoid;
        }}
        
        /* Metrics Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 2rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }}
        
        th {{
            background: linear-gradient(135deg, #ec4899, #f97316);
            color: white;
            font-weight: 600;
            padding: 1rem;
            text-align: left;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        td {{
            padding: 1rem;
            border-bottom: 1px solid #e2e8f0;
            font-size: 0.875rem;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        tr:nth-child(even) {{
            background: #f8fafc;
        }}
        
        /* Chart Section */
        .chart {{
            text-align: center;
            margin: 2rem 0;
            padding: 1.5rem;
            background: #f8fafc;
            border-radius: 8px;
        }}
        
        .chart img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        /* Content Paragraphs */
        p {{
            margin-bottom: 1rem;
            font-size: 0.875rem;
            line-height: 1.7;
        }}
        
        /* Footer */
        footer {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #64748b;
            font-size: 0.75rem;
        }}
        
        /* Print Styles */
        @media print {{
            .page {{
                padding: 1rem;
            }}
            
            
            h2 {{
                page-break-before: avoid;
                page-break-after: avoid;
            }}
            
            .chart {{
                page-break-inside: avoid;
            }}
            
            table {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <!-- Cover Page -->
        <div class="cover">
            
            <h1>Annual Impact Report</h1>
            
            <div class="year">{year}</div>
        </div>

        <!-- Executive Summary -->
        <h2>Executive Summary</h2>
        <div class="summary">{data['summary']}</div>

        <!-- Key Metrics -->
        <h2>Key Metrics</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Total Learners</td><td><strong>{data['stats']['total_learners']}</strong></td></tr>
                <tr><td>Support Partners</td><td><strong>{data['stats']['support_partners']}</strong></td></tr>
                <tr><td>Volunteer Hours</td><td><strong>{data['stats']['volunteer_hours']}</strong></td></tr>
                <tr><td>Active Volunteers</td><td><strong>{data['stats']['active_volunteers']}</strong></td></tr>
            </tbody>
        </table>

        <!-- Learner Impact Trend Chart -->
        <h2>Learner Impact Trend</h2>
        <div class="chart">
            <img src="data:image/png;base64,{img_base64}" alt="Learner Impact Trend Chart"/>
        </div>

        <!-- Course Learner Distribution -->
        <h2>Course Distribution</h2>
        <p>{dist_text}</p>

        <!-- Program Details -->
        <h2>Program Overview</h2>
        <div class="summary">{program_details_text}</div>

        <!-- Future Plans -->
        <h2>Future Plans</h2>
        <div class="summary">{future_text}</div>

        <!-- Footer -->
        <footer>
            <p><strong>ANALYSEA</strong> | Empowering Communities Through Data-Driven Impact</p>
            <p>contact@analysea.org | www.analysea.org</p>
        </footer>
    </div>
</body>
</html>
"""

    # Generate PDF into memory
    pdf_io = BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)

    return StreamingResponse(
        pdf_io,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=impact-report.pdf"}
    )