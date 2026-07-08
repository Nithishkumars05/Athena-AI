from models.base_model import BaseModel
import ollama


class OllamaModel(BaseModel):

    def __init__(self, model_name="qwen3:8b"):
        self.model_name = model_name


    def generate(self, user_name, message):
        try:

            prompt = f"""
You are Athena AI.

User: {user_name}

Message:
{message}
"""

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response["message"]["content"]


        except Exception as e:
            return f"Ollama Error: {str(e)}"