"""
Athena AI - Chat Prompt Builder

Responsible for constructing prompts
for normal conversations.

Uses ConversationService for:
- system prompt
- history

Does NOT communicate with AI models.
"""

from services.conversation_service import conversation_service
from .base_prompt_builder import BasePromptBuilder


class ChatPromptBuilder(BasePromptBuilder):

    def build(
        self,
        user_name: str,
        message: str,
    ) -> str:

        system_prompt = (
            conversation_service.load_system_prompt()
        )

        history = (
            conversation_service.load_history(
                user_name
            )
        )

        conversation = (
            conversation_service.format_history(
                history
            )
        )

        prompt = f"""
{system_prompt}

Conversation:
{conversation}

User:
{message}

Athena:
"""

        return prompt


chat_prompt_builder = ChatPromptBuilder()