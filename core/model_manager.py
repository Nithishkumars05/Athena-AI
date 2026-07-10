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

                capabilities=[
                    "chat",
                    "assistant",
                    "reasoning",
                    "vision",
                    "document"
                ],

                description=(
                    "Fast cloud model for general conversations "
                    "and multimodal tasks."
                ),

                supports_streaming=True,
                supports_vision=True,

                recommended_for=[
                    "General conversations",
                    "Reasoning",
                    "Image understanding",
                    "Documents"
                ],

                instance=GeminiModel()
            ),


            # ==========================
            # Offline Models
            # ==========================

            "qwen3:8b": ModelInfo(
                name="qwen3:8b",
                display_name="Qwen3 8B",
                provider="offline",

                capabilities=[
                    "chat",
                    "assistant"
                ],

                description=(
                    "Balanced offline model for everyday conversations."
                ),

                supports_streaming=True,
                supports_vision=False,

                recommended_for=[
                    "General conversations",
                    "Offline assistant tasks"
                ],

                instance=OllamaModel("qwen3:8b")
            ),


            "qwen2.5-coder:7b": ModelInfo(
                name="qwen2.5-coder:7b",
                display_name="Qwen2.5 Coder 7B",
                provider="offline",

                capabilities=[
                    "coding",
                    "debugging",
                    "programming"
                ],

                description=(
                    "Optimized model for programming "
                    "and software development."
                ),

                supports_streaming=True,
                supports_vision=False,

                recommended_for=[
                    "Code generation",
                    "Debugging",
                    "Programming assistance"
                ],

                instance=OllamaModel(
                    "qwen2.5-coder:7b"
                )
            ),


            "qwen3:14b": ModelInfo(
                name="qwen3:14b",
                display_name="Qwen3 14B",
                provider="offline",

                capabilities=[
                    "reasoning",
                    "analysis"
                ],

                description=(
                    "Large reasoning-focused offline model."
                ),

                supports_streaming=True,
                supports_vision=False,

                recommended_for=[
                    "Complex reasoning",
                    "Deep analysis"
                ],

                instance=OllamaModel(
                    "qwen3:14b"
                )
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


    def get_models_by_capability(self, capability: str):

        return [
            model
            for model in self.models.values()
            if capability in model.capabilities
        ]


    # ------------------------------------
    # Generation
    # ------------------------------------

    def generate(
    self,
    user_name: str,
    prompt: str,
    original_message: str | None = None,
):

        mode = settings.get_ai_mode()
        selected_model = settings.get_model()

        if mode == "auto":

            try:

                return self.models[
                "qwen3:8b"
            ].instance.generate(
                user_name=user_name,
                prompt=prompt,
                original_message=original_message,
            )

            except Exception:

                return self.models[
                "gemini-2.5-flash"
            ].instance.generate(
                user_name=user_name,
                prompt=prompt,
                original_message=original_message,
            )

        model_info = self.get_model(selected_model)

        if model_info is None:
            raise ValueError(
            f"Unknown model: {selected_model}"
        )

        if model_info.provider != mode:
            raise ValueError(
            f"Model '{selected_model}' "
            f"does not belong to '{mode}' mode."
        )

        return model_info.instance.generate(
        user_name=user_name,
        prompt=prompt,
        original_message=original_message,
    )

    # ------------------------------------
    # Streaming
    # ------------------------------------

    def stream_generate(
    self,
    user_name: str,
    prompt: str,
    original_message: str | None = None,
):

        mode = settings.get_ai_mode()
        selected_model = settings.get_model()

        if mode == "auto":

            try:

                yield from self.models[
                "qwen3:8b"
            ].instance.stream_generate(
                user_name=user_name,
                prompt=prompt,
                original_message=original_message,
            )

            except Exception:

                yield from self.models[
                "gemini-2.5-flash"
            ].instance.stream_generate(
                user_name=user_name,
                prompt=prompt,
                original_message=original_message,
            )

            return

        model_info = self.get_model(selected_model)

        if model_info is None:
            raise ValueError(
            f"Unknown model: {selected_model}"
        )

        if model_info.provider != mode:
            raise ValueError(
            f"Model '{selected_model}' "
            f"does not belong to '{mode}' mode."
        )

        yield from model_info.instance.stream_generate(
        user_name=user_name,
        prompt=prompt,
        original_message=original_message,
    )

    # ------------------------------------
    # Direct Model Generation
    # ------------------------------------

    def generate_with_model(
        self,
    model_name: str,
    user_name: str,
    prompt: str,
    original_message: str | None = None,
):

        model_info = self.get_model(model_name)

        if model_info is None:
            raise ValueError(
            f"Unknown model: {model_name}"
        )

        return model_info.instance.generate(
        user_name=user_name,
        prompt=prompt,
        original_message=original_message,
    )
    def stream_generate_with_model(
    self,
    model_name: str,
    user_name: str,
    prompt: str,
    original_message: str | None = None,
):

        model_info = self.get_model(model_name)

        if model_info is None:
            raise ValueError(
            f"Unknown model: {model_name}"
        )

        yield from model_info.instance.stream_generate(
        user_name=user_name,
        prompt=prompt,
        original_message=original_message,
    )

model_manager = ModelManager()