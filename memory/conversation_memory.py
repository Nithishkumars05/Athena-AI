"""
Athena AI
Conversation Memory

Responsible for persisting conversations.

Stores and loads conversations from disk.

Does NOT interact with AI models.
"""

from pathlib import Path
import json
from datetime import datetime

from core.conversation_manager import (
    Conversation,
    Message,
)


class ConversationMemory:

    def __init__(self):

        self.storage = Path("data/conversations")
        self.storage.mkdir(parents=True, exist_ok=True)

    # ---------------------------------
    # Save
    # ---------------------------------

    def save(self, conversation):

        data = {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                }
                for msg in conversation.messages
            ],
        }

        filepath = self.storage / f"{conversation.id}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ---------------------------------
    # Load
    # ---------------------------------

    def load(self, conversation_id):

        filepath = self.storage / f"{conversation_id}.json"

        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        conversation = Conversation(
            id=data["id"],
            title=data["title"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )

        for msg in data["messages"]:

            conversation.messages.append(
                Message(
                    role=msg["role"],
                    content=msg["content"],
                    timestamp=datetime.fromisoformat(msg["timestamp"]),
                )
            )

        return conversation

    # ---------------------------------
    # Load All
    # ---------------------------------

    def load_all(self):

        conversations = []

        for file in self.storage.glob("*.json"):

            conv = self.load(file.stem)

            if conv:
                conversations.append(conv)

        return conversations

    # ---------------------------------
    # Delete
    # ---------------------------------

    def delete(self, conversation_id):

        filepath = self.storage / f"{conversation_id}.json"

        if filepath.exists():
            filepath.unlink()


conversation_memory = ConversationMemory()