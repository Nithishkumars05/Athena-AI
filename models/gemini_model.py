from models.base_model import BaseModel

from app.config import client
from app.settings import settings
from services.conversation_service import conversation_service

class GeminiModel(BaseModel):


    def generate(self, user_name: str, message: str) -> str:

        # Save user message
        conversation_service.save_user_message(
        user_name,
        message
    )


        # Load system prompt
        prompt = conversation_service.build_prompt(
    user_name,
    message
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

            answer = (
                "Sorry, I couldn't generate a response."
            )



        conversation_service.save_ai_message(
        user_name,
        answer
)


        return answer