"""
Athena AI - Model Router

Responsible for selecting the best AI model
for a given task.

Does not execute models.
Delegates execution to ModelManager.

Uses model capabilities instead of hardcoded
model names.
"""

from app.settings import settings
from core.enums.task_type import TaskType
from core.logger import logger
from core.model_manager import model_manager


class ModelRouter:

    def select_model(
        self,
        task_type: TaskType,
    ):

        mode = settings.get_ai_mode()

        # --------------------------------
        # Manual Mode
        # --------------------------------

        if mode != "auto":

            selected_model = settings.get_model()

            logger.info(
                f"Model selected | {selected_model} | "
                "Mode=Manual"
            )

            return selected_model

        # --------------------------------
        # Capability Mapping
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
            "chat",
        )

        models = model_manager.get_models_by_capability(
            capability
        )

        # --------------------------------
        # No Matching Models
        # --------------------------------

        if not models:

            logger.warning(
                "No models found for capability '%s'. "
                "Using fallback model llama3.1:8b.",
                capability,
            )

            return "llama3.1:8b"

        # --------------------------------
        # Vision
        # --------------------------------

        if task_type == TaskType.VISION:

            for model in models:

                if model.name == "gemini-2.5-flash":

                    logger.info(
                        "Model selected | gemini-2.5-flash | Task=VISION"
                    )

                    return model.name

            for model in models:

                if model.name == "llava:latest":

                    logger.info(
                        "Model selected | llava:latest | Task=VISION | Fallback=Yes"
                    )

                    return model.name

        # --------------------------------
        # Coding
        # --------------------------------

        elif task_type == TaskType.CODING:

            for model in models:

                if model.name == "qwen2.5-coder:7b":

                    logger.info(
                        "Model selected | qwen2.5-coder:7b | Task=CODING"
                    )

                    return model.name

            for model in models:

                if model.name == "gemini-2.5-flash":

                    logger.info(
                        "Model selected | gemini-2.5-flash | Task=CODING | Fallback=Yes"
                    )

                    return model.name

        # --------------------------------
        # Reasoning / Math
        # --------------------------------

        elif task_type in (

            TaskType.REASONING,
            TaskType.MATH,

        ):

            for model in models:

                if model.name == "gemini-2.5-flash":

                    logger.info(
                        "Model selected | gemini-2.5-flash | Task=REASONING"
                    )

                    return model.name

            for model in models:

                if model.name == "qwen3:14b":

                    logger.info(
                        "Model selected | qwen3:14b | Task=REASONING | Fallback=Yes"
                    )

                    return model.name

        # --------------------------------
        # Chat
        # --------------------------------

        elif task_type == TaskType.CHAT:

            for model in models:

                if model.name == "gemini-2.5-flash":

                    logger.info(
                        "Model selected | gemini-2.5-flash | Task=CHAT"
                    )

                    return model.name

            for model in models:

                if model.name == "llama3.1:8b":

                    logger.info(
                        "Model selected | llama3.1:8b | Task=CHAT | Fallback=Yes"
                    )

                    return model.name

        # --------------------------------
        # Document
        # --------------------------------

        elif task_type == TaskType.DOCUMENT:

            for model in models:

                if model.name == "gemini-2.5-flash":

                    logger.info(
                        "Model selected | gemini-2.5-flash | Task=DOCUMENT"
                    )

                    return model.name

        # --------------------------------
        # Generic Offline Fallback
        # --------------------------------

        for model in models:

            if model.provider == "offline":

                logger.info(
                    f"Model selected | {model.name} | Generic Offline Fallback"
                )

                return model.name

        # --------------------------------
        # Final Fallback
        # --------------------------------

        logger.info(
            f"Model selected | {models[0].name} | Final Fallback"
        )

        return models[0].name


model_router = ModelRouter()