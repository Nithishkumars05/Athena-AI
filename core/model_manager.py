"""
Athena AI Core - Model Manager

Responsible for selecting and managing
the active AI model.
"""

from models.gemini_model import GeminiModel
from models.ollama_model import OllamaModel
from app.settings import settings


class ModelManager:

    def __init__(self):

        self.models = {

            # Cloud Model
            "gemini-2.5-flash": GeminiModel(),

            # Offline Models
            "qwen3:8b": OllamaModel("qwen3:8b"),

            "qwen2.5-coder:7b": OllamaModel("qwen2.5-coder:7b")
        }


        self.current_model = "gemini-2.5-flash"


    def set_model(self, model_name: str):

        if model_name not in self.models:
            raise ValueError(
                f"Unknown model: {model_name}"
            )

        self.current_model = model_name


    def get_current_model(self):

        return self.current_model


    def generate(self, user_name, message):

        mode = settings.get_ai_mode()

        if mode == "cloud":

            return self.models["gemini-2.5-flash"].generate(
                user_name,
                message
            )

        elif mode == "offline":

            return self.models["qwen3:8b"].generate(
                user_name,
                message
            )

        elif mode == "auto":

            try:

                return self.models["qwen3:8b"].generate(
                    user_name,
                    message
                )

            except Exception:

                return self.models["gemini-2.5-flash"].generate(
                    user_name,
                    message
             )

        else:

            model_name = settings.get_model()

            if model_name not in self.models:
                model_name = self.current_model

            return self.models[model_name].generate(
                user_name,
                message
            )


model_manager = ModelManager()