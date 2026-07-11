"""
Athena AI - Task Router

Responsible for identifying the type of task
the user wants to perform.

This does NOT select models.
It only classifies the task.
"""

import re

from core.enums.task_type import TaskType
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

        # -----------------------------
        # Image uploads always use Vision
        # -----------------------------
        if request.file_type == "image":
            return TaskType.VISION

        text = request.original_message.lower()

        for task, keywords in self.rules.items():

            for keyword in keywords:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    text,
                ):
                    return task

        return TaskType.CHAT


task_router = TaskRouter()