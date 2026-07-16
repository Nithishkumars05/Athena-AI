"""
Athena AI - Dispatcher
"""

from agents.intent_router import router

from models.chat_request import ChatRequest

from agents.chat_agent import (
    handle as chat_handle,
    stream_handle as chat_stream,
)

from agents.math_agent import handle as math_handle
from agents.report_agent import handle as report_handle
from agents.python_agent import handle as python_handle

class Dispatcher:

    def handle(self, request: ChatRequest) -> str:

        intent = router.detect(request.message)

        # -----------------------------
        # Math
        # -----------------------------
        if intent == "math":
            return math_handle(
                request.user_name,
                request.message
            )

        # -----------------------------
        # Report
        # -----------------------------
        if intent == "report":
            return report_handle(
                request.user_name,
                request.message
            )
        # -----------------------------
# Python
# -----------------------------
        if intent == "python":
            return python_handle(request)

        # -----------------------------
        # Documents
        # Any request with an attached file
        # is handled by the ChatAgent.
        # -----------------------------
        if request.file_path:
            return chat_handle(request)

        # -----------------------------
        # Normal Chat
        # -----------------------------
        return chat_handle(request)

    def stream_handle(self, request: ChatRequest):

        intent = router.detect(request.message)

        # -----------------------------
        # Math
        # -----------------------------
        if intent == "math":
            yield math_handle(
                request.user_name,
                request.message
            )
            return

        # -----------------------------
        # Report
        # -----------------------------
        if intent == "report":
            yield report_handle(
                request.user_name,
                request.message
            )
            return
        # -----------------------------
# Python
# -----------------------------
        if intent == "python":
            yield python_handle(request)
            return

        # -----------------------------
        # Documents
        # Any attached file goes through
        # the ChatAgent pipeline.
        # -----------------------------
        if request.file_path:
            yield from chat_stream(request)
            return

        # -----------------------------
        # Normal Chat
        # -----------------------------
        yield from chat_stream(request)


dispatcher = Dispatcher()