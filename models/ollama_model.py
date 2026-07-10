from models.base_model import BaseModel
from services.conversation_service import conversation_service
import ollama


class OllamaModel(BaseModel):

    def __init__(self, model_name="qwen3:8b"):
        self.model_name = model_name

    # -------------------------------------------------
    # Normal Generation
    # -------------------------------------------------

    def generate(
        self,
        user_name,
        prompt,
        original_message=None,
    ):

        try:

            conversation_service.save_user_message(
                user_name,
                original_message or prompt
            )

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

            conversation_service.save_ai_message(
                user_name,
                answer
            )

            return answer

        except Exception as e:

            return f"Ollama Error: {str(e)}"

    # -------------------------------------------------
    # Streaming
    # -------------------------------------------------

    def stream_generate(
        self,
        user_name,
        prompt,
        original_message=None,
    ):

        conversation_service.save_user_message(
            user_name,
            original_message or prompt
        )

        stream = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )

        full_response = ""

        for chunk in stream:

            text = chunk["message"]["content"]

            full_response += text

            yield text

        conversation_service.save_ai_message(
            user_name,
            full_response
        )