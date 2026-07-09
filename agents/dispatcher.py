"""
Athena AI - Dispatcher
"""

from agents.intent_router import router

from agents.chat_agent import (
    handle as chat_handle,
    stream_handle as chat_stream
)
from agents.math_agent import handle as math_handle
from agents.report_agent import handle as report_handle
from agents.document_agent import handle as document_handle


class Dispatcher:

    def handle(self, user_name: str, message: str) -> str:

        intent = router.detect(message)

        if intent == "math":
            return math_handle(user_name, message)

        elif intent == "report":
            return report_handle(user_name, message)

        elif intent == "document":
            return document_handle(user_name, message)

        else:
            return chat_handle(user_name, message)

    def stream_handle(self, user_name: str, message: str):

        intent = router.detect(message)

        if intent == "chat":

            yield from chat_stream(
            user_name,
            message
        )

        else:

            result = self.handle(
            user_name,
            message
        )

            yield result

dispatcher = Dispatcher()