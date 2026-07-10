from models.base_model import BaseModel

from app.config import client
from app.settings import settings
from services.conversation_service import conversation_service


class GeminiModel(BaseModel):

    def generate(self, user_name, prompt, original_message=None,):

        conversation_service.save_user_message(
            user_name,
            original_message or prompt
        )

        response = client.models.generate_content(
            model=settings.get_model(),
            contents=prompt,
            config={
                "temperature": settings.get_temperature()
            }
        )

        if hasattr(response, "text") and response.text:
            answer = response.text.strip()
        else:
            answer = "Sorry, I couldn't generate a response."

        conversation_service.save_ai_message(
            user_name,
            answer
        )

        return answer

    def stream_generate(self, user_name, prompt, original_message=None,):

        conversation_service.save_user_message(
            user_name,
            original_message or prompt
        )

        stream = client.models.generate_content_stream(
            model=settings.get_model(),
            contents=prompt,
            config={
                "temperature": settings.get_temperature()
            }
        )

        full_response = ""

        for chunk in stream:

            if hasattr(chunk, "text") and chunk.text:
                full_response += chunk.text
                yield chunk.text

        conversation_service.save_ai_message(
            user_name,
            full_response
        )