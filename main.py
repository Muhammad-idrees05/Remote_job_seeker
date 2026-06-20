"""
main.py

Remote ML Job Agent — FastAPI Backend

Run:
    uvicorn main:app --reload
"""

import os
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ──────────────────────────────────────────────────────────
# Environment
# ──────────────────────────────────────────────────────────

load_dotenv()

# ──────────────────────────────────────────────────────────
# Agent imports
# ──────────────────────────────────────────────────────────

from agents.linkedin_agent import search_remote_jobs
from agents.company_agent import analyze_company
from agents.resume_agent import analyze_resume
from agents.ats_agent import calculate_ats_score
from agents.email_agent import generate_email

# ──────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────

app = FastAPI(
    title="Remote ML Job Agent",
    version="1.0.0",
    description="Multi-Agent AI system for remote ML job search.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────
# Request models
# ──────────────────────────────────────────────────────────


class JobRequest(BaseModel):
    job_title: str
    country: str
    experience: str
    remote_only: bool
    skills: str


class CompanyRequest(BaseModel):
    company: str


class EmailRequest(BaseModel):
    company: str
    role: str
    skills: str


# ──────────────────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────────────────


@app.get("/")
def root():
    return {
        "status": "running",
        "application": "Remote ML Job Agent",
        "version": "1.0.0",
    }


# ──────────────────────────────────────────────────────────
# Job search
# ──────────────────────────────────────────────────────────


@app.post("/jobs")
async def jobs(request: JobRequest):
    try:
        results = search_remote_jobs(
            job_title=request.job_title,
            country=request.country,
            experience=request.experience,
            remote_only=request.remote_only,
            skills=request.skills,
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────────────────
# Company analysis
# ──────────────────────────────────────────────────────────


@app.post("/company")
async def company(request: CompanyRequest):
    try:
        result = analyze_company(request.company)
        return {"company": request.company, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────────────────
# ATS analysis
# ──────────────────────────────────────────────────────────


@app.post("/ats")
async def ats(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    skills: str = Form(...),
):
    temp_path = None
    try:
        suffix = resume.filename.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
            tmp.write(await resume.read())
            temp_path = tmp.name

        resume_text = analyze_resume(temp_path)
        result = calculate_ats_score(
            resume_text=resume_text,
            job_title=job_title,
            required_skills=skills,
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ──────────────────────────────────────────────────────────
# Email generator
# ──────────────────────────────────────────────────────────


@app.post("/email")
async def email(request: EmailRequest):
    try:
        result = generate_email(
            company=request.company,
            role=request.role,
            skills=request.skills,
        )
        return {"email": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────────────────
# Full multi-agent pipeline
# ──────────────────────────────────────────────────────────


@app.post("/full-analysis")
async def full_pipeline(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    country: str = Form(...),
    experience: str = Form(...),
    skills: str = Form(...),
):
    temp_path = None
    try:
        suffix = resume.filename.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
            tmp.write(await resume.read())
            temp_path = tmp.name

        jobs = search_remote_jobs(
            job_title=job_title,
            country=country,
            experience=experience,
            remote_only=True,
            skills=skills,
        )

        resume_text = analyze_resume(temp_path)

        ats = calculate_ats_score(
            resume_text=resume_text,
            job_title=job_title,
            required_skills=skills,
        )

        email_text = generate_email(
            company="Hiring Manager",
            role=job_title,
            skills=skills,
        )

        company_reports = []
        for job in jobs[:3]:
            company_reports.append({
                "company": job["company"],
                "analysis": analyze_company(job["company"]),
            })

        return {
            "jobs": jobs,
            "ats": ats,
            "companies": company_reports,
            "email": email_text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
