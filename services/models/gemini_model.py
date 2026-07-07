from services.models.base_model import BaseModel
from app.config import client
from app.memory import add_message, get_history


class GeminiModel(BaseModel):

    def format_history(self, history):
        return "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in history
        )

    def generate(self, user_name: str, message: str) -> str:

        # Save user message
        add_message(user_name, "User", message)

        # Load system prompt
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # Get recent history
        history = get_history(user_name)[-20:]

        conversation = self.format_history(history)

        prompt = f"""
{system_prompt}

Conversation:
{conversation}

Athena:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if hasattr(response, "text") and response.text:
            answer = response.text.strip()
        else:
            answer = "Sorry, I couldn't generate a response."

        add_message(user_name, "Athena", answer)

        return answer