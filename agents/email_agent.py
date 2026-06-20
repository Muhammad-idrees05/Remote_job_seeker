"""
agents/email_agent.py

Professional job application email generator
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)


def generate_email(company: str, role: str, skills: str) -> str:
    """
    Called by main.py (FastAPI /email endpoint).
    Generates a professional job application email.
    """
    prompt = f"""
Write a professional job application email for the following:

Target Company / Recipient: {company}
Role Applying For: {role}
Candidate Skills: {skills}

Requirements:
- Professional and concise tone
- Strong ML/AI engineering voice
- Highlight relevant skills naturally
- Include a clear call to action
- Keep it under 250 words
- Do NOT use placeholder brackets like [Your Name] — write it as a ready-to-send template

Output only the email body (no subject line).
"""
    response = llm.invoke(prompt)
    return response.content.strip()


def email_agent(job_title: str, company_analysis: list) -> str:
    """
    Called by graph.py (LangGraph node).
    Extracts company context then generates email.
    """
    company_names = ", ".join(
        [c.get("company", "") for c in company_analysis if c.get("company")]
    )
    skills_context = "\n".join(
        [c.get("analysis", "") for c in company_analysis[:2]]
    )

    return generate_email(
        company=company_names or "Hiring Manager",
        role=job_title,
        skills=skills_context
    )
