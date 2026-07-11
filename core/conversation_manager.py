"""
Athena AI - Conversation Manager

Maintains active conversation context.
"""

from collections import deque


class ConversationManager:

    def __init__(self):
        self.history = deque(maxlen=20)

    def add_message(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history.clear()


conversation_manager = ConversationManager()