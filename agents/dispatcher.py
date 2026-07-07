"""
Athena AI - Dispatcher

Acts as the central coordinator.

Flow:
User
 ↓
Dispatcher
 ↓
Intent Router
 ↓
Selected Agent
"""

from agents.intent_router import router
from agents.chat_agent import chat
from agents.math_agent import solve_equation
from agents.report_agent import create_report
from agents.document_agent import summarize_document


class Dispatcher:

    def handle(self, user_name: str, message: str) -> str:

        intent = router.detect(message)

        if intent == "math":
            return solve_equation(message)

        elif intent == "report":
            return create_report(message)

        elif intent == "document":
            return summarize_document(message)

        else:
            return chat(user_name, message)


dispatcher = Dispatcher()