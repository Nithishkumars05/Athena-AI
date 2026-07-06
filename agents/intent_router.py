"""
Athena AI - Intent Router
Routes user requests to the correct agent.
"""

import re


class IntentRouter:

    def __init__(self):

        self.intents = {

            "math": [
                "solve",
                "simplify",
                "differentiate",
                "derivative",
                "integrate",
                "integration",
                "factor",
                "expand",
                "equation",
                "calculate"
            ],

            "report": [
                "report",
                "essay",
                "article",
                "research",
                "write about"
            ],

            "document": [
                "summarize",
                "summary",
                "pdf",
                "document",
                "docx",
                "file"
            ]
        }

    def detect(self, text: str):

        text = text.lower()

        for intent, keywords in self.intents.items():

            for keyword in keywords:

                if re.search(rf"\b{re.escape(keyword)}\b", text):
                    return intent

        return "chat"


router = IntentRouter()

if __name__ == "__main__":

    tests = [

        "Solve x^2 + 5x + 6",

        "Generate a report on AI",

        "Summarize this pdf",

        "Who invented Python?",

        "Differentiate x^3",

        "Factor x^2+5x+6",

        "Tell me a joke"

    ]

    for t in tests:

        print(f"{t}")

        print("→", router.detect(t))

        print()