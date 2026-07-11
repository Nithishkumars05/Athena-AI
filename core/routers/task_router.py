"""
Athena AI - Task Router

Responsible for identifying the type of task
the user wants to perform.

This does NOT select models.
It only classifies the task.
"""

import re

from core.enums.task_type import TaskType
from core.logger import logger
from services.request_processor import ProcessedRequest


class TaskRouter:

    def __init__(self):

        self.rules = {

            TaskType.CODING: [
                "code",
                "python",
                "java",
                "javascript",
                "debug",
                "bug",
                "error",
                "function",
                "class",
                "program",
                "script",
                "algorithm"
            ],

            TaskType.MATH: [
                "calculate",
                "solve",
                "equation",
                "derivative",
                "integral",
                "factor",
                "simplify"
            ],

            TaskType.DOCUMENT: [
                "pdf",
                "document",
                "summarize",
                "summary",
                "docx",
                "file"
            ],

            TaskType.REASONING: [
                "analyze",
                "analyse",
                "compare",
                "explain deeply",
                "why",
                "reason",
                "evaluate"
            ],

            TaskType.VISION: [
                "image",
                "picture",
                "photo",
                "screenshot",
                "diagram"
            ]
        }

    def classify(
        self,
        request: ProcessedRequest,
    ) -> TaskType:
        """
        Determine the task type from the processed request.
        """

        # ---------------------------------
        # Image uploads always use Vision
        # ---------------------------------

        if request.file_type == "image":

            logger.info(
                "Task detected | VISION | Reason=Image Upload"
            )

            return TaskType.VISION

        # ---------------------------------
        # Safely process message
        # ---------------------------------

        text = (request.original_message or "").lower()

        # ---------------------------------
        # Keyword matching
        # ---------------------------------

        for task, keywords in self.rules.items():

            for keyword in keywords:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    text,
                ):

                    logger.info(
                        f"Task detected | {task.name} | "
                        f"Keyword='{keyword}'"
                    )

                    return task

        # ---------------------------------
        # Default Chat
        # ---------------------------------

        logger.info(
            "Task detected | CHAT | Reason=Default"
        )

        return TaskType.CHAT


task_router = TaskRouter()