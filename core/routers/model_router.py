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

            TaskType.CODING:
                "coding",

            TaskType.REASONING:
                "reasoning",

            TaskType.VISION:
                "vision",

            TaskType.MATH:
                "reasoning",

            TaskType.DOCUMENT:
                "document",

            TaskType.CHAT:
                "chat"
        }


        capability = capability_map.get(
            task_type,
            "chat"
        )


        # --------------------------------
        # Find compatible models
        # --------------------------------

        models = (
            model_manager
            .get_models_by_capability(
                capability
            )
        )


        if not models:

            # fallback
            return (
                settings.get_model()
                or "qwen3:8b"
            )


        # --------------------------------
        # Select best candidate
        # --------------------------------

        for model in models:

            if model.provider == "offline":

                return model.name


        # If no offline model exists,
        # use first available

        return models[0].name



model_router = ModelRouter()