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
from agents.document_agent import handle as document_handle


class Dispatcher:

    def handle(self, request: ChatRequest) -> str:

        intent = router.detect(request.message)

        if intent == "math":
            return math_handle(
                request.user_name,
                request.message
            )

        if intent == "report":
            return report_handle(
                request.user_name,
                request.message
            )

        if intent == "document":
            return document_handle(
                request.user_name,
                request.message
            )

        return chat_handle(request)

    def stream_handle(self, request: ChatRequest):
        """
        Stream responses whenever the selected
        agent supports it.
        """

        intent = router.detect(request.message)

        if intent == "chat":
            yield from chat_stream(request)
            return

        yield self.handle(request)


dispatcher = Dispatcher()