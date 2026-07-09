from models.base_model import BaseModel
from services.conversation_service import conversation_service
import ollama


class OllamaModel(BaseModel):

    def __init__(self, model_name="qwen3:8b"):
        self.model_name = model_name


    def generate(self, user_name, message):
        try:

            conversation_service.save_user_message(
    user_name,
    message
)

            prompt = conversation_service.build_prompt(
        user_name,
        message
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
        
    def stream_generate(self, user_name: str, message: str):

        conversation_service.save_user_message(
        user_name,
        message
    )

        prompt = conversation_service.build_prompt(
        user_name,
        message
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