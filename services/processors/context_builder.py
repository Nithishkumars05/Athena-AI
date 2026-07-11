"""
Athena AI
Context Builder

Builds the complete prompt sent to AI models.

Does NOT perform inference.
Does NOT choose models.
"""

from core.conversation_manager import conversation_manager


class ContextBuilder:

    SYSTEM_PROMPT = """You are Athena AI.

You are a professional desktop AI assistant.

Be accurate, concise and helpful.
Remember the conversation context when answering.
"""

    def build(self, user_message: str) -> str:

        messages = conversation_manager.get_messages()

        prompt = [
            self.SYSTEM_PROMPT,
            "",
            "Conversation:",
            "-------------",
        ]

        # Include only the most recent messages
        history = messages[-10:]

        for message in history:
            role = message.role.capitalize()
            prompt.append(f"{role}: {message.content}")

        prompt.extend([
            "",
            "User:",
            user_message,
            "",
            "Assistant:"
        ])

        return "\n".join(prompt)


context_builder = ContextBuilder()