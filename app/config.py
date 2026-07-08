import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY=os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in the .env file")

client=genai.Client(api_key=API_KEY)
# ==========================================
# AI Configuration
# ==========================================

AI_MODE = "cloud"      # cloud | offline | auto

GEMINI_MODEL = "gemini-2.5-flash"

OLLAMA_CHAT_MODEL = "qwen3:8b"

OLLAMA_CODE_MODEL = "qwen2.5-coder:7b"

OLLAMA_URL = "http://localhost:11434"