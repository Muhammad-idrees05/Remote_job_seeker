"""
agents/reflection.py

Reflection agent — reviews pipeline output and suggests improvements
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)


def reflection_agent(state: dict) -> dict:
    """
    Reviews the full pipeline output and suggests improvements.
    """
    ats = state.get("ats_score", {})
    score = ats.get("score", "N/A") if isinstance(ats, dict) else "N/A"
    missing = ats.get("missing", []) if isinstance(ats, dict) else []

    prompt = f"""
You are a career coaching AI performing a reflection review.

Pipeline output summary:
- Plan: {state.get('plan', 'N/A')}
- ATS Score: {score}/100
- Missing Skills: {', '.join(missing) if missing else 'None identified'}
- Companies Analyzed: {len(state.get('company_analysis', []))}
- Email Generated: {'Yes' if state.get('email') else 'No'}

Provide 3–5 specific, actionable improvements the candidate should make to:
1. Increase their ATS score
2. Better target job listings
3. Strengthen their application email

Be direct and constructive.
"""
    response = llm.invoke(prompt)

    return {
        "reflection": response.content.strip()
    }
