import os
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# AI MODE
# =====================================================

AI_MODE = os.getenv("AI_MODE", "auto")

# =====================================================
# CLOUD
# =====================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# =====================================================
# OLLAMA
# =====================================================

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

OLLAMA_CHAT_MODEL = os.getenv(
    "OLLAMA_CHAT_MODEL",
    "qwen3:8b"
)

OLLAMA_CODE_MODEL = os.getenv(
    "OLLAMA_CODE_MODEL",
    "qwen2.5-coder:7b"
)

OLLAMA_REASONING_MODEL = os.getenv(
    "OLLAMA_REASONING_MODEL",
    "qwen3:14b"
)

OLLAMA_VISION_MODEL = os.getenv(
    "OLLAMA_VISION_MODEL",
    "llava:latest"
)

OLLAMA_EMBED_MODEL = os.getenv(
    "OLLAMA_EMBED_MODEL",
    "nomic-embed-text:latest"
)