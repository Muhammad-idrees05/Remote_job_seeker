"""
app.py

Remote ML Job Agent
Frontend: Streamlit

Run:
    streamlit run app.py
"""

import streamlit as st
import requests
import json

# ──────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Remote ML Job Agent",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://localhost:8000"

# ──────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────

st.sidebar.title("🤖 Remote ML Job Agent")
st.sidebar.markdown("---")

country = st.sidebar.selectbox(
    "Preferred Country",
    ["Worldwide", "USA", "Canada", "Germany", "United Kingdom",
     "Australia", "Netherlands", "Singapore"],
)

experience = st.sidebar.selectbox(
    "Experience",
    ["Intern", "Junior", "1-2 Years", "3-5 Years", "Senior"],
)

remote_only = st.sidebar.checkbox("Remote Only", value=True)

# ──────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────

st.title("🤖 Agentic AI Remote ML Job Assistant")
st.markdown("""
- 🔍 Search Remote Machine Learning Jobs
- 📄 Analyze Resume
- 🎯 Get ATS Score
- 📧 Generate Professional Email
- 🏢 Research Companies
""")
st.divider()

# ──────────────────────────────────────────────────────────
# SEARCH FORM
# ──────────────────────────────────────────────────────────

job_title = st.text_input("Job Title", value="Machine Learning Engineer")

skills = st.text_area(
    "Skills",
    value="Python\nMachine Learning\nDeep Learning\nPyTorch\nTensorFlow\n"
          "Computer Vision\nNLP\nFastAPI\nDocker\nLangChain\nLangGraph",
)

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ──────────────────────────────────────────────────────────
# BUTTONS
# ──────────────────────────────────────────────────────────

col1, col2, col3 = st.columns(3)
search_button = col1.button("🔍 Find Jobs")
ats_button = col2.button("📄 ATS Analysis")
email_button = col3.button("📧 Generate Email")
st.divider()

# ──────────────────────────────────────────────────────────
# FIND JOBS
# ──────────────────────────────────────────────────────────

if search_button:
    with st.spinner("Searching Remote Jobs..."):
        payload = {
            "job_title": job_title,
            "country": country,
            "experience": experience,
            "remote_only": remote_only,
            "skills": skills,
        }
        try:
            response = requests.post(f"{API_URL}/jobs", json=payload)
            if response.status_code == 200:
                jobs = response.json()
                st.success(f"✅ {len(jobs)} Jobs Found")
                for job in jobs:
                    st.subheader(job.get("title", "Untitled"))
                    st.write("🏢", job.get("company", "Unknown"))
                    st.write("🌍", job.get("location", "Remote"))
                    st.write(job.get("description", ""))
                    if job.get("url"):
                        st.link_button("Apply Now", job["url"])
                    st.divider()
            else:
                st.error(f"Backend Error: {response.text}")
        except Exception as e:
            st.error(str(e))

# ──────────────────────────────────────────────────────────
# ATS ANALYSIS
# ──────────────────────────────────────────────────────────

if ats_button:
    if resume is None:
        st.warning("Please upload a resume PDF first.")
    else:
        with st.spinner("Analyzing Resume..."):
            try:
                response = requests.post(
                    f"{API_URL}/ats",
                    files={"resume": (resume.name, resume, "application/pdf")},
                    data={"job_title": job_title, "skills": skills},
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ ATS Report Ready")
                    st.metric("ATS Score", f"{result.get('score', 0)}%")

                    st.subheader("✅ Matched Skills")
                    for skill in result.get("matched", []):
                        st.success(skill)

                    st.subheader("❌ Missing Skills")
                    for skill in result.get("missing", []):
                        st.error(skill)

                    st.subheader("💡 Suggestions")
                    st.write(result.get("suggestions", ""))
                else:
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(str(e))

# ──────────────────────────────────────────────────────────
# EMAIL GENERATOR
# ──────────────────────────────────────────────────────────

if email_button:
    with st.spinner("Generating Email..."):
        payload = {
            "company": "Hiring Manager",
            "role": job_title,
            "skills": skills,
        }
        try:
            response = requests.post(f"{API_URL}/email", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Professional Email Generated")
                st.text_area("Email", value=result.get("email", ""), height=350)
                st.download_button(
                    "⬇️ Download Email",
                    result.get("email", ""),
                    file_name="job_application_email.txt",
                )
            else:
                st.error(f"Backend Error: {response.text}")
        except Exception as e:
            st.error(str(e))

# ──────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────

st.divider()
st.markdown("""
### 🚀 Tech Stack
- **Groq LLM** (llama-3.3-70b-versatile)
- **LangGraph** Multi-Agent Workflow
- **FastAPI** Backend
- **Streamlit** Frontend
- **ChromaDB** Memory
- **Tavily** Search API

*Made with ❤️ using Agentic AI*
""")
