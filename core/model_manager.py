"""
Athena AI Core - Model Manager

Responsible for selecting and managing
the active AI model.
"""

from models.gemini_model import GeminiModel
from models.ollama_model import OllamaModel
from app.settings import settings
from core.model_info import ModelInfo

class ModelManager:

    def __init__(self):

        self.models = {

        "gemini-2.5-flash": ModelInfo(
            name="gemini-2.5-flash",
            provider="cloud",
            instance=GeminiModel()
        ),

        "qwen3:8b": ModelInfo(
            name="qwen3:8b",
            provider="offline",
            instance=OllamaModel("qwen3:8b")
        ),

        "qwen2.5-coder:7b": ModelInfo(
            name="qwen2.5-coder:7b",
            provider="offline",
            instance=OllamaModel("qwen2.5-coder:7b")
        ),

        "qwen3:14b": ModelInfo(
            name="qwen3:14b",
            provider="offline",
            instance=OllamaModel("qwen3:14b")
        )
    }

    def set_model(self, model_name: str):

        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")

        settings.set_model(model_name)


    def get_current_model(self):

        return settings.get_model()

    def generate(self, user_name: str, message: str):

        mode = settings.get_ai_mode()
        selected_model = settings.get_model()

    # -------------------------
    # AUTO MODE
    # -------------------------

        if mode == "auto":

            try:
                return self.models["qwen3:8b"].instance.generate(
                user_name,
                message
            )

            except Exception:

                return self.models["gemini-2.5-flash"].instance.generate(
                user_name,
                message
            )

    # -------------------------
    # Validate Selected Model
    # -------------------------

        model_info = self.models.get(selected_model)

        if model_info is None:
            raise ValueError(
            f"Unknown model: {selected_model}"
        )

    # -------------------------
    # Validate Provider
    # -------------------------

        if model_info.provider != mode:

            raise ValueError(
            f"Model '{selected_model}' does not belong to '{mode}' mode."
        )

    # -------------------------
    # Generate
    # -------------------------

        return model_info.instance.generate(
            user_name,
            message
    )
model_manager = ModelManager()