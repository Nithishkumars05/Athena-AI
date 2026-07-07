"""
Athena AI Core - Model Manager

Responsible for selecting and managing
the active AI model.
"""

from models.gemini_model import GeminiModel
from app.settings import settings

class ModelManager:

    def __init__(self):
        self.models = {
            "gemini-2.5-flash": GeminiModel()
        }

        self.current_model = "gemini-2.5-flash"

    def set_model(self, model_name: str):
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")

        self.current_model = model_name

    def get_current_model(self):
        return self.current_model

    def generate(self, user_name, message):
        model = settings.get_model()
        return self.models[model].generate(user_name, message)
    


model_manager = ModelManager()