"""
Athena AI

Workspace Model

Represents a logical collection of conversations.
Future features:
- Workspace specific memory
- Workspace specific documents
- Workspace specific settings
- Workspace specific agents
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import uuid


@dataclass
class Workspace:

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    name: str = "New Workspace"

    description: str = ""

    icon: str = "📁"

    color: str = "#4F8EF7"

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    conversation_ids: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )

    archived: bool = False

    # --------------------------------------------------
    # Serialization
    # --------------------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "color": self.color,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "conversation_ids": self.conversation_ids,
            "metadata": self.metadata,
            "archived": self.archived,
        }

    # --------------------------------------------------

    @classmethod
    def from_dict(cls, data):

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "New Workspace"),
            description=data.get("description", ""),
            icon=data.get("icon", "📁"),
            color=data.get("color", "#4F8EF7"),
            created_at=data.get(
                "created_at",
                datetime.now().isoformat()
            ),
            updated_at=data.get(
                "updated_at",
                datetime.now().isoformat()
            ),
            conversation_ids=data.get(
                "conversation_ids",
                []
            ),
            metadata=data.get(
                "metadata",
                {}
            ),
            archived=data.get(
                "archived",
                False
            ),
        )