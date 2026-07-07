from services.models.gemini_model import GeminiModel


class ModelManager:

    def __init__(self):
        self.models = {
            "gemini": GeminiModel()
        }

        self.current_model = "gemini"

    def set_model(self, model_name: str):
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")

        self.current_model = model_name

    def get_current_model(self):
        return self.current_model

    def generate(self, user_name: str, message: str):
        return self.models[self.current_model].generate(
            user_name,
            message
        )


model_manager = ModelManager()