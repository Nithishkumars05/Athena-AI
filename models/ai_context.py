"""
Athena AI - AI Context

Represents all contextual information
required to answer a user's request.

Every AI provider should receive an
AIContext before formatting prompts.
"""

from dataclasses import dataclass, field


@dataclass
class AIContext:

    # Core
    system_prompt: str
    user_message: str

    # Conversation
    history: list[str] = field(default_factory=list)

    # Documents
    document_text: str | None = None
    image_path: str | None = None

    # Metadata
    metadata: dict = field(default_factory=dict)