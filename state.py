"""
state.py

Shared state for LangGraph multi-agent system
"""

from typing import TypedDict, List, Dict, Any, Optional


class JobState(TypedDict):
    """
    Central state object passed between all agents.
    """

    # ── User input ──────────────────────────────────────────
    job_title: str
    country: str
    experience: str
    skills: str
    resume_path: Optional[str]

    # ── Agent outputs ────────────────────────────────────────
    plan: str                               # planner_agent output
    jobs: List[Dict[str, Any]]              # search_jobs_agent output
    company_analysis: List[Dict[str, Any]]  # company_analysis_agent output
    resume_text: str                        # resume_agent output
    ats_score: Dict[str, Any]              # ats_agent output
    email: str                              # email_agent output
    reflection: str                         # reflection_agent output

    # ── Workflow tracking ────────────────────────────────────
    current_step: str
    next_step: str
    logs: List[str]

    # ── Memory ───────────────────────────────────────────────
    memory: Dict[str, Any]
