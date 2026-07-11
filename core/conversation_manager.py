"""
Athena AI
Conversation Manager

Responsible for managing all chat sessions.

Does NOT perform AI inference.
Does NOT summarize conversations.

Only stores and retrieves conversations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Message:

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Conversation:

    id: str
    title: str
    created_at: datetime
    messages: list[Message] = field(default_factory=list)


class ConversationManager:

    def __init__(self):

        self._conversations = {}
        self._current = None

    # -----------------------------
    # Conversation Operations
    # -----------------------------

    def new_conversation(self, title="New Chat"):

        conv = Conversation(
            id=str(uuid4()),
            title=title,
            created_at=datetime.now(),
        )

        self._conversations[conv.id] = conv
        self._current = conv.id

        return conv

    def get_current(self):

        if self._current is None:
            return None

        return self._conversations[self._current]

    def set_current(self, conversation_id):

        if conversation_id in self._conversations:
            self._current = conversation_id

    def all_conversations(self):

        return list(self._conversations.values())

    # -----------------------------
    # Message Operations
    # -----------------------------

    def add_message(self, role, content):

        conv = self.get_current()

        if conv is None:
            conv = self.new_conversation()

        conv.messages.append(
            Message(
                role=role,
                content=content
            )
        )

    def get_messages(self):

        conv = self.get_current()

        if conv is None:
            return []

        return conv.messages

    def clear_current(self):

        conv = self.get_current()

        if conv:
            conv.messages.clear()

    def delete_conversation(self, conversation_id):

        if conversation_id in self._conversations:

            del self._conversations[conversation_id]

            if self._current == conversation_id:
                self._current = None


conversation_manager = ConversationManager()