"""
agents/ats_agent.py

ATS (Applicant Tracking System) scoring agent
"""

import sys
import os
import json
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)


def calculate_ats_score(
    resume_text: str,
    job_title: str,
    required_skills: str
) -> dict:
    """
    Called by main.py (FastAPI /ats endpoint).
    Returns parsed ATS result dict with score, matched, missing, suggestions.
    """
    prompt = f"""
You are an ATS (Applicant Tracking System).

Analyze this resume against the job requirements and return ONLY valid JSON — no markdown, no explanation.

Resume:
{resume_text}

Target Job Title: {job_title}

Required Skills:
{required_skills}

Return this exact JSON structure:
{{
  "score": <integer 0-100>,
  "matched": [<list of matched skills as strings>],
  "missing": [<list of missing skills as strings>],
  "suggestions": "<actionable improvement suggestions as a single string>"
}}
"""
    response = llm.invoke(prompt)
    raw = response.content.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return safe defaults so the API never 500s
        result = {
            "score": 0,
            "matched": [],
            "missing": [],
            "suggestions": raw  # surface raw text for debugging
        }

    return result


def ats_agent(resume_text: str, jobs: list) -> dict:
    """
    Called by graph.py (LangGraph node).
    Builds job description from job list then scores.
    """
    job_titles = ", ".join([j.get("title", "") for j in jobs])
    job_skills = " ".join([j.get("description", "") for j in jobs])

    return calculate_ats_score(
        resume_text=resume_text,
        job_title=job_titles,
        required_skills=job_skills
    )
