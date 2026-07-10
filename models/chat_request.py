"""
Athena AI - Chat Request

Represents a single chat request travelling
through the Olympus-7 pipeline.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatRequest:
    user_name: str
    message: str
    file_path: Optional[str] = None