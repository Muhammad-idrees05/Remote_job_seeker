"""
app.py
Remote ML Job Agent - Professional UI
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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
        border-right: 1px solid #0f3460;
    }

    /* Cards */
    .job-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #0f3460;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .job-card:hover {
        border-color: #e94560;
        box-shadow: 0 8px 32px rgba(233, 69, 96, 0.2);
        transform: translateY(-2px);
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 16px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #0f3460) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4) !important;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1a1a2e !important;
        border: 1px solid #0f3460 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 12px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #e94560 !important;
        box-shadow: 0 0 0 2px rgba(233, 69, 96, 0.2) !important;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        background: #1a1a2e !important;
        border: 1px solid #0f3460 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #1a1a2e !important;
        border: 2px dashed #0f3460 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1a2e !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* Divider */
    hr {
        border-color: #0f3460 !important;
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, rgba(233,69,96,0.1), rgba(15,52,96,0.3));
        border-radius: 20px;
        border: 1px solid #0f3460;
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(135deg, #e94560, #a8edea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 1.2em;
        color: #a0aec0;
        margin-bottom: 0;
    }

    /* Feature badges */
    .badge {
        display: inline-block;
        background: rgba(233,69,96,0.15);
        border: 1px solid rgba(233,69,96,0.3);
        border-radius: 20px;
        padding: 6px 16px;
        margin: 4px;
        font-size: 13px;
        color: #e94560;
        font-weight: 500;
    }

    /* Score bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #e94560, #a8edea) !important;
        border-radius: 10px !important;
    }

    /* Section headers */
    .section-header {
        font-size: 1.4em;
        font-weight: 700;
        color: #e94560;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #0f3460;
    }

    /* Stats row */
    .stat-box {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #0f3460;
    }

    .stat-number {
        font-size: 2em;
        font-weight: 800;
        color: #e94560;
    }

    .stat-label {
        color: #a0aec0;
        font-size: 0.9em;
    }

    /* Success/Error/Warning overrides */
    .stSuccess {
        background: rgba(72, 199, 142, 0.1) !important;
        border: 1px solid rgba(72, 199, 142, 0.3) !important;
        border-radius: 10px !important;
    }

    .stError {
        background: rgba(233, 69, 96, 0.1) !important;
        border: 1px solid rgba(233, 69, 96, 0.3) !important;
        border-radius: 10px !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────

if "groq_key" not in st.session_state:
    try:
        st.session_state.groq_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.session_state.groq_key = os.getenv("GROQ_API_KEY", "")

if "tavily_key" not in st.session_state:
    try:
        st.session_state.tavily_key = st.secrets["TAVILY_API_KEY"]
    except Exception:
        st.session_state.tavily_key = os.getenv("TAVILY_API_KEY", "")

GROQ_MODEL = "llama-3.3-70b-versatile"

# ──────────────────────────────────────────────────────────
# LOCATIONS
# ──────────────────────────────────────────────────────────

LOCATIONS = {
    "🌍 Worldwide": ["Worldwide"],
    "🇺🇸 USA": [
        "USA - All", "New York", "San Francisco", "Seattle",
        "Austin", "Boston", "Chicago", "Los Angeles", "Remote USA"
    ],
    "🇨🇦 Canada": [
        "Canada - All", "Toronto", "Vancouver", "Montreal",
        "Calgary", "Ottawa", "Remote Canada"
    ],
    "🇩🇪 Germany": [
        "Germany - All", "Berlin", "Munich", "Hamburg",
        "Frankfurt", "Cologne", "Remote Germany"
    ],
    "🇬🇧 United Kingdom": [
        "UK - All", "London", "Manchester", "Edinburgh",
        "Birmingham", "Bristol", "Remote UK"
    ],
    "🇦🇺 Australia": [
        "Australia - All", "Sydney", "Melbourne", "Brisbane",
        "Perth", "Adelaide", "Remote Australia"
    ],
    "🇳🇱 Netherlands": [
        "Netherlands - All", "Amsterdam", "Rotterdam",
        "The Hague", "Utrecht", "Remote Netherlands"
    ],
    "🇸🇬 Singapore": [
        "Singapore - All", "Central Singapore", "Remote Singapore"
    ],
    "🇵🇰 Pakistan": [
        "Pakistan - All", "Karachi", "Lahore", "Islamabad",
        "Rawalpindi", "Faisalabad", "Remote Pakistan"
    ],
}

# ──────────────────────────────────────────────────────────
# AGENT FUNCTIONS
# ──────────────────────────────────────────────────────────

def get_llm_response(prompt: str) -> str:
    from langchain_groq import ChatGroq
    llm = ChatGroq(api_key=st.session_state.groq_key, model=GROQ_MODEL)
    response = llm.invoke(prompt)
    return response.content.strip()


def search_remote_jobs(job_title, location, experience, remote_only, skills):
    from tavily import TavilyClient
    client = TavilyClient(api_key=st.session_state.tavily_key)
    remote = "remote" if remote_only else ""
    query = f"{remote} {job_title} jobs {location} {experience} {skills}".strip()
    results = client.search(query=query, max_results=10)
    jobs = []
    for r in results.get("results", []):
        jobs.append({
            "title": r.get("title", job_title),
            "company": r.get("source", "Unknown"),
            "description": r.get("content", ""),
            "url": r.get("url", ""),
            "location": f"Remote ({location})" if remote_only else location,
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

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0;'>
        <div style='font-size: 3em;'>🤖</div>
        <div style='font-size: 1.3em; font-weight: 800; color: #e94560;'>ML Job Agent</div>
        <div style='font-size: 0.8em; color: #a0aec0;'>Powered by Groq + LangChain</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌍 Location")

    country_choice = st.selectbox(
        "Country",
        list(LOCATIONS.keys()),
        label_visibility="collapsed"
    )

    city_choice = st.selectbox(
        "City",
        LOCATIONS[country_choice],
        label_visibility="collapsed"
    )

    st.markdown("### 💼 Experience")
    experience = st.selectbox(
        "Experience Level",
        ["Intern", "Junior", "1-2 Years", "3-5 Years", "Senior"],
        label_visibility="collapsed"
    )

    st.markdown("### ⚙️ Options")
    remote_only = st.checkbox("🌐 Remote Only", value=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding: 10px 0;'>
        <div style='color: #a0aec0; font-size: 0.8em;'>
            🚀 Tech Stack<br>
            <span style='color: #e94560;'>Groq</span> · 
            <span style='color: #e94560;'>LangChain</span> · 
            <span style='color: #e94560;'>Tavily</span><br>
            <span style='color: #e94560;'>Streamlit</span> · 
            <span style='color: #e94560;'>PyPDF</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HERO SECTION
# ──────────────────────────────────────────────────────────

st.markdown("""
<div class='hero'>
    <h1>🤖 Remote ML Job Agent</h1>
    <p>Your AI-powered career assistant for Machine Learning jobs worldwide</p>
    <br>
    <span class='badge'>🔍 Job Search</span>
    <span class='badge'>📄 ATS Scoring</span>
    <span class='badge'>📧 Email Generator</span>
    <span class='badge'>🌐 Remote First</span>
    <span class='badge'>🧠 AI Powered</span>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# INPUTS
# ──────────────────────────────────────────────────────────

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("#### 💼 Job Title")
    job_title = st.text_input(
        "Job Title",
        value="Machine Learning Engineer",
        label_visibility="collapsed",
        placeholder="e.g. ML Engineer, Data Scientist..."
    )

    st.markdown("#### 🛠️ Your Skills")
    skills = st.text_area(
        "Skills",
        value="Python\nMachine Learning\nDeep Learning\nPyTorch\nTensorFlow\n"
              "Computer Vision\nNLP\nFastAPI\nDocker\nLangChain\nLangGraph",
        height=220,
        label_visibility="collapsed",
        placeholder="Enter one skill per line..."
    )

with col_right:
    st.markdown("#### 📄 Upload Resume")
    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        label_visibility="collapsed",
        help="Upload your resume PDF for ATS analysis"
    )

    if resume:
        st.markdown(f"""
        <div style='background: rgba(72,199,142,0.1); border: 1px solid rgba(72,199,142,0.3);
             border-radius: 10px; padding: 12px; margin-top: 10px;'>
            ✅ <strong>{resume.name}</strong> uploaded successfully
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📍 Selected Location")
    st.markdown(f"""
    <div style='background: rgba(15,52,96,0.5); border: 1px solid #0f3460;
         border-radius: 10px; padding: 16px; margin-top: 8px;'>
        <div style='font-size: 1.1em; font-weight: 600;'>{country_choice}</div>
        <div style='color: #a0aec0; font-size: 0.9em;'>📍 {city_choice}</div>
        <div style='color: #a0aec0; font-size: 0.9em;'>💼 {experience}</div>
        <div style='color: #e94560; font-size: 0.9em;'>{"🌐 Remote Only" if remote_only else "🏢 On-site / Hybrid"}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# ACTION BUTTONS
# ──────────────────────────────────────────────────────────

col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    search_button = st.button("🔍 Find Jobs", use_container_width=True)
with col2:
    ats_button = st.button("📄 ATS Analysis", use_container_width=True)
with col3:
    email_button = st.button("📧 Generate Email", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# FIND JOBS
# ──────────────────────────────────────────────────────────

if search_button:
    if not st.session_state.tavily_key:
        st.error("❌ Tavily API Key not found. Please set it in your .env file or Streamlit Secrets.")
    else:
        with st.spinner(f"🔍 Searching {job_title} jobs in {city_choice}..."):
            try:
                jobs = search_remote_jobs(
                    job_title=job_title,
                    location=city_choice,
                    experience=experience,
                    remote_only=remote_only,
                    skills=skills,
                )
                st.markdown(f"""
                <div class='section-header'>
                    🎯 Found {len(jobs)} Jobs in {city_choice}
                </div>
                """, unsafe_allow_html=True)

                for i, job in enumerate(jobs):
                    st.markdown(f"""
                    <div class='job-card'>
                        <div style='font-size: 1.2em; font-weight: 700; color: #ffffff; margin-bottom: 8px;'>
                            {job.get('title', 'Untitled')}
                        </div>
                        <div style='display: flex; gap: 20px; margin-bottom: 12px;'>
                            <span style='color: #a0aec0;'>🏢 {job.get('company', 'Unknown')}</span>
                            <span style='color: #e94560;'>🌍 {job.get('location', city_choice)}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander(f"📄 View Description — {job.get('title', '')}"):
                        st.write(job.get("description", "No description available."))
                        if job.get("url"):
                            st.link_button("🚀 Apply Now", job["url"])

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ──────────────────────────────────────────────────────────
# ATS ANALYSIS
# ──────────────────────────────────────────────────────────

if ats_button:
    if resume is None:
        st.warning("⚠️ Please upload your resume PDF first.")
    elif not st.session_state.groq_key:
        st.error("❌ Groq API Key not found. Please set it in your .env file or Streamlit Secrets.")
    else:
        with st.spinner("🧠 Analyzing your resume with AI..."):
            try:
                resume_text = analyze_resume_pdf(resume)
                result = calculate_ats_score(
                    resume_text=resume_text,
                    job_title=job_title,
                    required_skills=skills,
                )

                st.markdown("<div class='section-header'>📊 ATS Analysis Report</div>", unsafe_allow_html=True)

                score = result.get("score", 0)
                color = "#48c78e" if score >= 70 else "#ffdd57" if score >= 50 else "#e94560"

                st.markdown(f"""
                <div style='text-align: center; padding: 30px;
                     background: linear-gradient(135deg, #1a1a2e, #0f3460);
                     border-radius: 16px; border: 1px solid #0f3460; margin-bottom: 20px;'>
                    <div style='font-size: 4em; font-weight: 800; color: {color};'>{score}%</div>
                    <div style='color: #a0aec0; font-size: 1.1em;'>ATS Compatibility Score</div>
                    <div style='margin-top: 10px; color: {color}; font-weight: 600;'>
                        {"🟢 Excellent Match!" if score >= 70 else "🟡 Good Match" if score >= 50 else "🔴 Needs Improvement"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.progress(score / 100)
                st.markdown("<br>", unsafe_allow_html=True)

                col1, col2 = st.columns(2, gap="large")
                with col1:
                    st.markdown("#### ✅ Matched Skills")
                    for skill in result.get("matched", []):
                        st.markdown(f"""
                        <div style='background: rgba(72,199,142,0.1); border: 1px solid rgba(72,199,142,0.3);
                             border-radius: 8px; padding: 8px 14px; margin: 4px 0; color: #48c78e;'>
                            ✓ {skill}
                        </div>
                        """, unsafe_allow_html=True)

                with col2:
                    st.markdown("#### ❌ Missing Skills")
                    for skill in result.get("missing", []):
                        st.markdown(f"""
                        <div style='background: rgba(233,69,96,0.1); border: 1px solid rgba(233,69,96,0.3);
                             border-radius: 8px; padding: 8px 14px; margin: 4px 0; color: #e94560;'>
                            ✗ {skill}
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 💡 AI Suggestions")
                st.markdown(f"""
                <div style='background: rgba(15,52,96,0.5); border: 1px solid #0f3460;
                     border-left: 4px solid #e94560; border-radius: 10px; padding: 20px;'>
                    {result.get('suggestions', '')}
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ──────────────────────────────────────────────────────────
# EMAIL GENERATOR
# ──────────────────────────────────────────────────────────

if email_button:
    if not st.session_state.groq_key:
        st.error("❌ Groq API Key not found. Please set it in your .env file or Streamlit Secrets.")
    else:
        with st.spinner("✍️ Crafting your professional email..."):
            try:
                email_text = generate_email(
                    company="Hiring Manager",
                    role=job_title,
                    skills=skills,
                )

                st.markdown("<div class='section-header'>📧 Professional Application Email</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1a1a2e, #16213e);
                     border: 1px solid #0f3460; border-radius: 16px; padding: 30px;
                     font-family: Georgia, serif; line-height: 1.8; color: #e2e8f0;
                     white-space: pre-wrap;'>
                    {email_text}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "⬇️ Download Email",
                        email_text,
                        file_name="job_application_email.txt",
                        use_container_width=True,
                    )
                with col_b:
                    st.text_area(
                        "Copy Email",
                        value=email_text,
                        height=200,
                        label_visibility="collapsed"
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ──────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 30px;
     background: linear-gradient(135deg, #1a1a2e, #16213e);
     border-radius: 16px; border: 1px solid #0f3460;'>
    <div style='color: #e94560; font-size: 1.2em; font-weight: 700; margin-bottom: 10px;'>
        🤖 Remote ML Job Agent
    </div>
    <div style='color: #a0aec0; font-size: 0.9em; margin-bottom: 16px;'>
        Built with Agentic AI · LangGraph · Groq LLM · Tavily Search
    </div>
    <div>
        <span style='background: rgba(233,69,96,0.15); border: 1px solid rgba(233,69,96,0.3);
              border-radius: 20px; padding: 4px 12px; margin: 3px; font-size: 12px; color: #e94560;'>
              Groq LLM
        </span>
        <span style='background: rgba(233,69,96,0.15); border: 1px solid rgba(233,69,96,0.3);
              border-radius: 20px; padding: 4px 12px; margin: 3px; font-size: 12px; color: #e94560;'>
              LangChain
        </span>
        <span style='background: rgba(233,69,96,0.15); border: 1px solid rgba(233,69,96,0.3);
              border-radius: 20px; padding: 4px 12px; margin: 3px; font-size: 12px; color: #e94560;'>
              Tavily
        </span>
        <span style='background: rgba(233,69,96,0.15); border: 1px solid rgba(233,69,96,0.3);
              border-radius: 20px; padding: 4px 12px; margin: 3px; font-size: 12px; color: #e94560;'>
              Streamlit
        </span>
        <span style='background: rgba(233,69,96,0.15); border: 1px solid rgba(233,69,96,0.3);
              border-radius: 20px; padding: 4px 12px; margin: 3px; font-size: 12px; color: #e94560;'>
              PyPDF
        </span>
    </div>
</div>
""", unsafe_allow_html=True)