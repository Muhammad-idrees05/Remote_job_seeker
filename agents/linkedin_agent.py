"""
agents/linkedin_agent.py

Job search agent using Tavily
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tavily import TavilyClient
from config import TAVILY_API_KEY, MAX_JOBS

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_remote_jobs(
    job_title: str,
    country: str,
    experience: str,
    remote_only: bool,
    skills: str
) -> list:
    """
    Called by main.py (FastAPI endpoints).
    Searches for remote jobs using Tavily.
    """
    remote_flag = "remote" if remote_only else ""
    query = f"{remote_flag} {job_title} jobs {country} {experience} {skills}"

    results = client.search(query=query.strip(), max_results=MAX_JOBS)

    jobs = []
    for r in results.get("results", []):
        jobs.append({
            "title": r.get("title", job_title),
            "company": r.get("source", "Unknown"),
            "description": r.get("content", ""),
            "url": r.get("url", ""),
            "location": "Remote" if remote_only else country,
        })

    return jobs


def search_jobs_agent(state: dict) -> list:
    """
    Called by graph.py (LangGraph node).
    Wraps search_remote_jobs using LangGraph state dict.
    """
    return search_remote_jobs(
        job_title=state.get("job_title", ""),
        country=state.get("country", "Worldwide"),
        experience=state.get("experience", ""),
        remote_only=True,
        skills=state.get("skills", ""),
    )
