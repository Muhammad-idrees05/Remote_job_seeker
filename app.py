"""
app.py

Remote ML Job Agent - Streamlit Cloud Standalone Version
No FastAPI backend needed
"""

import streamlit as st
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Remote ML Job Agent",
    page_icon="🤖",
    layout="wide"
)

# ──────────────────────────────────────────────────────────
# API KEYS
# ──────────────────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

# ──────────────────────────────────────────────────────────
# AGENT FUNCTIONS
# ──────────────────────────────────────────────────────────

def get_llm_response(prompt: str) -> str:
    from langchain_groq import ChatGroq
    llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)
    response = llm.invoke(prompt)
    return response.content.strip()


def search_remote_jobs(job_title, country, experience, remote_only, skills):
    from tavily import TavilyClient
    client = TavilyClient(api_key=TAVILY_API_KEY)
    remote = "remote" if remote_only else ""
    query = f"{remote} {job_title} jobs {country} {experience} {skills}".strip()
    results = client.search(query=query, max_results=10)
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


def calculate_ats_score(resume_text, job_title, required_skills):
    prompt = f"""
You are an ATS system. Analyze this resume and return ONLY valid JSON, no markdown, no explanation.

Resume:
{resume_text}

Target Job: {job_title}
Required Skills: {required_skills}

Return exactly this JSON:
{{
  "score": <integer 0-100>,
  "matched": [<list of matched skill strings>],
  "missing": [<list of missing skill strings>],
  "suggestions": "<actionable improvement suggestions as a single string>"
}}
"""
    raw = get_llm_response(prompt)
    raw = re.sub(r"^```(?:json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        return {"score": 0, "matched": [], "missing": [], "suggestions": raw}


def generate_email(company, role, skills):
    prompt = f"""
Write a professional job application email.

Company / Recipient: {company}
Role: {role}
Candidate Skills: {skills}

Requirements:
- Professional and concise tone
- Strong ML/AI engineering voice
- Clear call to action
- Under 250 words
- No placeholder brackets like [Your Name]
- Ready to send

Output only the email body.
"""
    return get_llm_response(prompt)


def analyze_resume_pdf(uploaded_file):
    import tempfile
    from pypdf import PdfReader
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    reader = PdfReader(tmp_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    os.remove(tmp_path)
    return text.strip()


# ──────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────

st.sidebar.title("🤖 Remote ML Job Agent")
st.sidebar.markdown("---")

country = st.sidebar.selectbox(
    "Preferred Country",
    ["Worldwide", "USA", "Canada", "Germany", "United Kingdom",
     "Australia", "Netherlands", "Singapore", "Pakistan"],
)

experience = st.sidebar.selectbox(
    "Experience Level",
    ["Intern", "Junior", "1-2 Years", "3-5 Years", "Senior"],
)

remote_only = st.sidebar.checkbox("Remote Only", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 API Keys")
st.sidebar.markdown("*Skip if already set in Streamlit secrets*")

if not GROQ_API_KEY:
    groq_input = st.sidebar.text_input("Groq API Key", type="password")
    if groq_input:
        GROQ_API_KEY = groq_input

if not TAVILY_API_KEY:
    tavily_input = st.sidebar.text_input("Tavily API Key", type="password")
    if tavily_input:
        TAVILY_API_KEY = tavily_input

# ──────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────

st.title("🤖 Agentic AI Remote ML Job Assistant")
st.markdown("""
- 🔍 Search Remote Machine Learning Jobs
- 📄 Analyze Resume & Get ATS Score
- 📧 Generate Professional Application Email
- 🏢 Research Target Companies
""")
st.divider()

# ──────────────────────────────────────────────────────────
# INPUTS
# ──────────────────────────────────────────────────────────

job_title = st.text_input("Job Title", value="Machine Learning Engineer")

skills = st.text_area(
    "Your Skills (one per line)",
    value="Python\nMachine Learning\nDeep Learning\nPyTorch\nTensorFlow\n"
          "Computer Vision\nNLP\nFastAPI\nDocker\nLangChain\nLangGraph",
    height=200,
)

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ──────────────────────────────────────────────────────────
# BUTTONS
# ──────────────────────────────────────────────────────────

col1, col2, col3 = st.columns(3)
search_button = col1.button("🔍 Find Jobs", use_container_width=True)
ats_button = col2.button("📄 ATS Analysis", use_container_width=True)
email_button = col3.button("📧 Generate Email", use_container_width=True)
st.divider()

# ──────────────────────────────────────────────────────────
# FIND JOBS
# ──────────────────────────────────────────────────────────

if search_button:
    if not TAVILY_API_KEY:
        st.error("❌ Please enter your Tavily API Key in the sidebar.")
    else:
        with st.spinner("🔍 Searching remote jobs..."):
            try:
                jobs = search_remote_jobs(
                    job_title=job_title,
                    country=country,
                    experience=experience,
                    remote_only=remote_only,
                    skills=skills,
                )
                st.success(f"✅ Found {len(jobs)} jobs")
                for job in jobs:
                    with st.container():
                        st.subheader(job.get("title", "Untitled"))
                        col_a, col_b = st.columns(2)
                        col_a.write(f"🏢 **{job.get('company', 'Unknown')}**")
                        col_b.write(f"🌍 **{job.get('location', 'Remote')}**")
                        with st.expander("📄 View Description"):
                            st.write(job.get("description", ""))
                        if job.get("url"):
                            st.link_button("🚀 Apply Now", job["url"])
                        st.divider()
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ──────────────────────────────────────────────────────────
# ATS ANALYSIS
# ──────────────────────────────────────────────────────────

if ats_button:
    if resume is None:
        st.warning("⚠️ Please upload your resume PDF first.")
    elif not GROQ_API_KEY:
        st.error("❌ Please enter your Groq API Key in the sidebar.")
    else:
        with st.spinner("📄 Analyzing resume..."):
            try:
                resume_text = analyze_resume_pdf(resume)
                result = calculate_ats_score(
                    resume_text=resume_text,
                    job_title=job_title,
                    required_skills=skills,
                )
                st.success("✅ ATS Report Ready")

                score = result.get("score", 0)
                st.metric("🎯 ATS Score", f"{score}%")
                st.progress(score / 100)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Matched Skills")
                    for skill in result.get("matched", []):
                        st.success(skill)
                with col2:
                    st.subheader("❌ Missing Skills")
                    for skill in result.get("missing", []):
                        st.error(skill)

                st.subheader("💡 Suggestions")
                st.info(result.get("suggestions", ""))

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ──────────────────────────────────────────────────────────
# EMAIL GENERATOR
# ──────────────────────────────────────────────────────────

if email_button:
    if not GROQ_API_KEY:
        st.error("❌ Please enter your Groq API Key in the sidebar.")
    else:
        with st.spinner("📧 Generating professional email..."):
            try:
                email_text = generate_email(
                    company="Hiring Manager",
                    role=job_title,
                    skills=skills,
                )
                st.success("✅ Email Generated")
                st.text_area("📧 Your Application Email", value=email_text, height=350)
                st.download_button(
                    "⬇️ Download Email",
                    email_text,
                    file_name="job_application_email.txt",
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ──────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────

st.divider()
st.markdown("""
### 🚀 Tech Stack
`Groq LLM` · `LangChain` · `LangGraph` · `Tavily Search` · `Streamlit` · `PyPDF` · `Python`

*Made with ❤️ using Agentic AI*
""")