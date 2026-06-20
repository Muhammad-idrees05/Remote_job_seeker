"""
agents/supervisor.py

Supervisor agent — determines next workflow step based on state
"""


def supervisor_agent(state: dict) -> dict:
    """
    Inspects current state and routes to the next required agent node.
    """
    logs = state.get("logs", [])
    logs.append("Supervisor checking workflow state")

    if not state.get("jobs"):
        next_step = "jobs"
    elif not state.get("company_analysis"):
        next_step = "company"
    elif not state.get("resume_text"):
        next_step = "resume"
    elif not state.get("ats_score"):
        next_step = "ats"
    elif not state.get("email"):
        next_step = "email"
    else:
        next_step = "done"

    logs.append(f"Supervisor routing to: {next_step}")

    return {
        "next_step": next_step,
        "logs": logs
    }
