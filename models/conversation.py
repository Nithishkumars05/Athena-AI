from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Conversation:

    id: str

    title: str = "New Chat"

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    messages: list = field(default_factory=list)

    # Conversation metadata

    pinned: bool = False

    folder: str = "General"

    archived: bool = False

    deleted: bool = False

    tags: list = field(default_factory=list)

    def touch(self):

        self.updated_at = datetime.now().isoformat()