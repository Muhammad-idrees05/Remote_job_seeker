"""
config.py

Central configuration for Remote ML Job Agent
"""

import os
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------

load_dotenv()

# -------------------------
# API KEYS
# -------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# -------------------------
# LLM CONFIGURATION
# -------------------------

GROQ_MODEL = "llama-3.3-70b-versatile"

# Alternative models you can switch to:
# GROQ_MODEL = "llama-3.1-8b-instant"
# GROQ_MODEL = "mixtral-8x7b-32768"

# -------------------------
# APP SETTINGS
# -------------------------

APP_NAME = "Remote ML Job Agent"
APP_VERSION = "1.0.0"

# -------------------------
# AGENT SETTINGS
# -------------------------

MAX_JOBS = 10
MAX_COMPANIES = 5

ENABLE_MEMORY = True
ENABLE_REFLECTION = True

# -------------------------
# VECTOR DB SETTINGS
# -------------------------

CHROMA_DB_PATH = "./memory/chroma"

# -------------------------
# SEARCH SETTINGS
# -------------------------

SEARCH_TOP_K = 5

# -------------------------
# VALIDATION CHECKS
# -------------------------

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing in .env file")

if not TAVILY_API_KEY:
    print("⚠️ Warning: TAVILY_API_KEY is missing (job search may fail)")

# -------------------------
# HELPER FUNCTION
# -------------------------

def get_config():
    """
    Returns all config values as dictionary
    Useful for debugging and logging
    """
    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "model": GROQ_MODEL,
        "max_jobs": MAX_JOBS,
        "enable_memory": ENABLE_MEMORY,
    }
