"""
agents/resume_agent.py

Resume parser agent using pypdf
"""

from pypdf import PdfReader


def analyze_resume(resume_path: str) -> str:
    """
    Called by main.py (FastAPI endpoints).
    Extracts text from a PDF resume.
    """
    reader = PdfReader(resume_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def resume_agent(resume_path: str) -> str:
    """
    Called by graph.py (LangGraph node).
    Alias for analyze_resume.
    """
    return analyze_resume(resume_path)
