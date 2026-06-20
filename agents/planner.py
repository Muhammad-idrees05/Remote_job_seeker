"""
agents/planner.py

Planner agent — builds an execution plan from user input
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)


def planner_agent(state: dict) -> dict:
    """
    Called by graph.py (LangGraph planner node).
    Generates a high-level search + application plan from state inputs.
    """
    prompt = f"""
You are a job search strategist AI.

User is looking for:
- Job Title: {state.get('job_title', 'Machine Learning Engineer')}
- Country: {state.get('country', 'Worldwide')}
- Experience: {state.get('experience', 'Mid-level')}
- Skills: {state.get('skills', '')}

Create a concise action plan (3–5 bullet points) to:
1. Find the best remote ML job matches
2. Tailor the resume and ATS score
3. Target the right companies
4. Write a compelling application email

Output only the bullet-point plan.
"""
    response = llm.invoke(prompt)

    return {
        "plan": response.content.strip(),
        "current_step": "planner_done",
        "logs": state.get("logs", []) + [f"Plan created: {response.content[:80]}..."]
    }
