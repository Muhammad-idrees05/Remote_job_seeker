"""
agents/company_agent.py

Company analysis agent using Groq LLM
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL, MAX_COMPANIES

llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)


def analyze_company(company: str) -> str:
    """
    Called by main.py (FastAPI /company endpoint).
    Analyzes a single company by name.
    """
    prompt = f"""
Analyze this company for a Machine Learning Engineer role:

Company: {company}

Provide:
- Company overview
- AI/ML focus areas
- Tech stack
- Hiring difficulty
- Culture and work environment
- Fit score for ML engineers (0-100)

Be concise and factual.
"""
    response = llm.invoke(prompt)
    return response.content


def company_analysis_agent(jobs: list) -> list:
    """
    Called by graph.py (LangGraph node).
    Analyzes top companies from job listings.
    """
    analyses = []

    for job in jobs[:MAX_COMPANIES]:
        prompt = f"""
Analyze this company for an ML Engineer role:

Company: {job.get('company', 'Unknown')}
Job Title: {job.get('title', '')}
Job Description: {job.get('description', '')}

Provide:
- Company overview
- AI/ML focus
- Tech stack
- Hiring difficulty
- Fit score (0-100)
"""
        response = llm.invoke(prompt)
        analyses.append({
            "company": job.get("company", "Unknown"),
            "analysis": response.content
        })

    return analyses
