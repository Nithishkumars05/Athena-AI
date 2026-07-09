"""
Athena AI - Conversation Service

Responsible for:

- Loading system prompt
- Loading conversation history
- Saving messages
- Building prompts

Every AI model should use this service.
"""

from app.memory import add_message, get_history
from app.settings import settings


class ConversationService:

    def load_history(self, user_name):

        history_limit = settings.get_history()

        return get_history(user_name)[-history_limit:]

    def format_history(self, history):

        return "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in history
        )

    def save_user_message(self, user_name, message):

        add_message(
            user_name,
            "User",
            message
        )

    def build_prompt(self, user_name, message):

        system_prompt = self.load_system_prompt()

        history = self.load_history(user_name)

        conversation = self.format_history(history)

        prompt = f"""
{system_prompt}

Conversation:
{conversation}

User:
{message}

Athena:
"""

        return prompt

    def load_system_prompt(self):

        with open(
        "prompts/system_prompt.txt",
        "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    def save_ai_message(self, user_name, message):

        add_message(
            user_name,
            "Athena",
            message
        )


conversation_service = ConversationService()