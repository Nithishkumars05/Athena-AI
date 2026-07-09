"""
Athena AI - Model Router

Responsible for selecting the best AI model
for a given task.

Does not execute models.
Delegates execution to ModelManager.
"""


from core.enums.task_type import TaskType
from core.model_manager import model_manager
from app.settings import settings


class ModelRouter:


    def select_model(self, task_type: TaskType):

        """
        Select the best model based on:

        - AI mode
        - Task type
        - Model capabilities
        """


        mode = settings.get_ai_mode()


        # --------------------------------
        # Manual selection mode
        # --------------------------------

        if mode != "auto":

            return settings.get_model()



        # --------------------------------
        # Automatic routing
        # --------------------------------

        if task_type == TaskType.CODING:

            return "qwen2.5-coder:7b"


        if task_type == TaskType.REASONING:

            return "qwen3:14b"


        if task_type == TaskType.VISION:

            return "gemini-2.5-flash"


        if task_type == TaskType.MATH:

            return "qwen3:14b"


        # Default

        return "qwen3:8b"



model_router = ModelRouter()