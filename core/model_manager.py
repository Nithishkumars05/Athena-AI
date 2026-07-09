"""
Athena AI Core - Model Manager

Responsible for registering and managing
all available AI models.
"""

from models.gemini_model import GeminiModel
from models.ollama_model import OllamaModel

from app.settings import settings
from core.model_info import ModelInfo


class ModelManager:

    def __init__(self):

        self.models = {

            # ==========================
            # Cloud Models
            # ==========================

            "gemini-2.5-flash": ModelInfo(
                name="gemini-2.5-flash",
                display_name="Gemini 2.5 Flash",
                provider="cloud",
                category="chat",
                description="Fast cloud model for general conversations.",
                supports_streaming=True,
                supports_vision=True,
                recommended_for="General chat, reasoning and images.",
                instance=GeminiModel()
            ),

            # ==========================
            # Offline Models
            # ==========================

            "qwen3:8b": ModelInfo(
                name="qwen3:8b",
                display_name="Qwen3 8B",
                provider="offline",
                category="chat",
                description="Balanced offline chat model.",
                supports_streaming=True,
                supports_vision=False,
                recommended_for="General offline conversations.",
                instance=OllamaModel("qwen3:8b")
            ),

            "qwen2.5-coder:7b": ModelInfo(
                name="qwen2.5-coder:7b",
                display_name="Qwen2.5 Coder 7B",
                provider="offline",
                category="coding",
                description="Optimized for programming and debugging.",
                supports_streaming=True,
                supports_vision=False,
                recommended_for="Code generation and debugging.",
                instance=OllamaModel("qwen2.5-coder:7b")
            ),

            "qwen3:14b": ModelInfo(
                name="qwen3:14b",
                display_name="Qwen3 14B",
                provider="offline",
                category="reasoning",
                description="Larger reasoning-focused offline model.",
                supports_streaming=True,
                supports_vision=False,
                recommended_for="Complex reasoning and analysis.",
                instance=OllamaModel("qwen3:14b")
            )
        }

    # ------------------------------------
    # Model Lookup
    # ------------------------------------

    def get_model(self, model_name: str):

        return self.models.get(model_name)

    def get_all_models(self):

        return list(self.models.values())

    def get_models_by_provider(self, provider: str):

        return [
            model
            for model in self.models.values()
            if model.provider == provider
        ]

    def get_models_by_category(self, category: str):

        return [
            model
            for model in self.models.values()
            if model.category == category
        ]

    # ------------------------------------
    # Generation
    # ------------------------------------

    def generate(self, user_name: str, message: str):

        mode = settings.get_ai_mode()
        selected_model = settings.get_model()

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

        model_info = self.get_model(selected_model)

        if model_info is None:
            raise ValueError(
                f"Unknown model: {selected_model}"
            )

        if model_info.provider != mode:
            raise ValueError(
                f"Model '{selected_model}' does not belong to '{mode}' mode."
            )

        return model_info.instance.generate(
            user_name,
            message
        )

    # ------------------------------------
    # Streaming
    # ------------------------------------

    def stream_generate(self, user_name: str, message: str):

        mode = settings.get_ai_mode()
        selected_model = settings.get_model()

        if mode == "auto":

            try:

                yield from self.models["qwen3:8b"].instance.stream_generate(
                    user_name,
                    message
                )

            except Exception:

                yield from self.models["gemini-2.5-flash"].instance.stream_generate(
                    user_name,
                    message
                )

            return

        model_info = self.get_model(selected_model)

        if model_info is None:
            raise ValueError(
                f"Unknown model: {selected_model}"
            )

        if model_info.provider != mode:
            raise ValueError(
                f"Model '{selected_model}' does not belong to '{mode}' mode."
            )

        yield from model_info.instance.stream_generate(
            user_name,
            message
        )

    def generate_with_model(
        self,
        model_name: str,
        user_name: str,
        message: str
    ):

        model_info = self.get_model(model_name)

        if model_info is None:
            raise ValueError(
            f"Unknown model: {model_name}"
        )

        return model_info.instance.generate(
        user_name,
        message
    )

    def stream_generate_with_model(
        self,
        model_name: str,
        user_name: str,
        message: str
    ):

        model_info = self.get_model(model_name)

        if model_info is None:
            raise ValueError(
            f"Unknown model: {model_name}"
        )

            yield from model_info.instance.stream_generate(
        user_name,
        message
    )


model_manager = ModelManager()