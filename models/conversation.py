from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Conversation:

    id: str

    title: str = "New Chat"

    created_at: str = field(
        default_factory=lambda:
        datetime.now().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda:
        datetime.now().isoformat()
    )

    messages: List[dict] = field(
        default_factory=list
    )

    # ==============================
    # Athena Intelligence Metadata
    # ==============================

    pinned: bool = False

    folder: str = "General"

    tags: List[str] = field(
        default_factory=list
    )


    def touch(self):

        self.updated_at = (
            datetime.now()
            .isoformat()
        )