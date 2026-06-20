"""
graph.py

LangGraph orchestration for Remote ML Job Agent
"""

from langgraph.graph import StateGraph, END

from agents.planner import planner_agent
from agents.linkedin_agent import search_jobs_agent
from agents.company_agent import company_analysis_agent
from agents.resume_agent import resume_agent
from agents.ats_agent import ats_agent
from agents.email_agent import email_agent
from agents.reflection import reflection_agent

from state import JobState


# ──────────────────────────────────────────────────────────
# Node wrappers
# ──────────────────────────────────────────────────────────

def planner_node(state: JobState) -> JobState:
    state["logs"].append("Planner started")
    result = planner_agent(state)
    state.update(result)
    return state


def job_search_node(state: JobState) -> JobState:
    state["logs"].append("Searching jobs")
    state["jobs"] = search_jobs_agent(state)
    return state


def company_node(state: JobState) -> JobState:
    state["logs"].append("Analyzing companies")
    state["company_analysis"] = company_analysis_agent(state["jobs"])
    return state


def resume_node(state: JobState) -> JobState:
    state["logs"].append("Processing resume")
    state["resume_text"] = resume_agent(state["resume_path"])
    return state


def ats_node(state: JobState) -> JobState:
    state["logs"].append("Calculating ATS score")
    state["ats_score"] = ats_agent(
        resume_text=state["resume_text"],
        jobs=state["jobs"]
    )
    return state


def email_node(state: JobState) -> JobState:
    state["logs"].append("Generating email")
    state["email"] = email_agent(
        job_title=state["job_title"],
        company_analysis=state["company_analysis"]
    )
    return state


def reflection_node(state: JobState) -> JobState:
    state["logs"].append("Running reflection")
    result = reflection_agent(state)
    state.update(result)
    return state


# ──────────────────────────────────────────────────────────
# Build graph
# ──────────────────────────────────────────────────────────

workflow = StateGraph(JobState)

workflow.add_node("planner", planner_node)
workflow.add_node("jobs", job_search_node)
workflow.add_node("company", company_node)
workflow.add_node("resume", resume_node)
workflow.add_node("ats", ats_node)
workflow.add_node("email", email_node)
workflow.add_node("reflection", reflection_node)

# Entry point
workflow.set_entry_point("planner")

# Linear flow
workflow.add_edge("planner", "jobs")
workflow.add_edge("jobs", "company")
workflow.add_edge("company", "resume")
workflow.add_edge("resume", "ats")
workflow.add_edge("ats", "email")
workflow.add_edge("email", "reflection")
workflow.add_edge("reflection", END)

# Compile
graph = workflow.compile()
