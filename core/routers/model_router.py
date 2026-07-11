"""
Athena AI - Model Router

Responsible for selecting the best AI model
for a given task.

Does not execute models.
Delegates execution to ModelManager.

Uses model capabilities instead of hardcoded
model names.
"""


from core.enums.task_type import TaskType
from core.model_manager import model_manager
from app.settings import settings



class ModelRouter:


    def select_model(
    self,
    task_type: TaskType
):
        """
    Select the best available model.

    Routing is based on:
    - AI mode
    - Task capability
    - Registered models
    """

        mode = settings.get_ai_mode()

    # --------------------------------
    # Manual selection mode
    # --------------------------------

        if mode != "auto":
            return settings.get_model()

    # --------------------------------
    # Capability mapping
    # --------------------------------

        capability_map = {

        TaskType.CODING: "coding",

        TaskType.REASONING: "reasoning",

        TaskType.VISION: "vision",

        TaskType.MATH: "reasoning",

        TaskType.DOCUMENT: "document",

        TaskType.CHAT: "chat",
    }

        capability = capability_map.get(
        task_type,
        "chat"
    )

        models = model_manager.get_models_by_capability(
        capability
    )

        if not models:
            return "qwen3:8b"

    # --------------------------------
    # Preferred routing
    # --------------------------------

        if task_type == TaskType.VISION:

        # Prefer offline LLaVA
            for model in models:
                if model.name == "llava:latest":
                    return model.name

        # Fall back to Gemini Vision
            for model in models:
                if model.name == "gemini-2.5-flash":
                    return model.name

        elif task_type == TaskType.CODING:

            for model in models:
                if model.name == "qwen2.5-coder:7b":
                    return model.name

        elif task_type in (
        TaskType.REASONING,
        TaskType.MATH,
    ):

            for model in models:
                if model.name == "qwen3:14b":
                    return model.name

        elif task_type == TaskType.CHAT:

            for model in models:
                if model.name == "qwen3:8b":
                    return model.name

        elif task_type == TaskType.DOCUMENT:

        # Prefer Gemini because it already supports
        # long-context document understanding.
            for model in models:
                if model.name == "gemini-2.5-flash":
                    return model.name

    # --------------------------------
    # Generic fallback
    # --------------------------------

        for model in models:
            if model.provider == "offline":
                return model.name

        return models[0].name


model_router = ModelRouter()