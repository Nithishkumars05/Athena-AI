"""
Athena AI - Intent Router

Routes user requests to the correct agent.

Priority Order
--------------
1. Python
2. Math
3. Report
4. Document
5. Chat
"""

import re


class IntentRouter:

    def __init__(self):

        self.intents = {

            # --------------------------------------------------
            # Python (Highest Priority)
            # --------------------------------------------------

            "python": [

                "python",
                "code",
                "program",
                "script",
                "execute",
                "run python",
                "write python",
                "generate python",
                "plot",
                "pandas",
                "numpy",
                "matplotlib",
                "csv",
                "dataframe",

            ],

            # --------------------------------------------------
            # Math
            # --------------------------------------------------

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
                "calculate",

            ],

            # --------------------------------------------------
            # Report
            # --------------------------------------------------

            "report": [

                "report",
                "essay",
                "article",
                "research",
                "write about",

            ],

            # --------------------------------------------------
            # Document
            # --------------------------------------------------

            "document": [

                "summarize",
                "summary",
                "pdf",
                "document",
                "docx",
                "file",

            ],
        }

    # --------------------------------------------------
    # Detect Intent
    # --------------------------------------------------

    def detect(
        self,
        text: str,
    ):

        text = text.lower().strip()

        # ==========================================
        # Python gets absolute priority
        # ==========================================

        for keyword in self.intents["python"]:

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                text,
            ):
                return "python"

        # ==========================================
        # Remaining intents
        # ==========================================

        for intent, keywords in self.intents.items():

            if intent == "python":
                continue

            for keyword in keywords:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    text,
                ):
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

        "Tell me a joke",

        "Write Python code to sort a list",

        "Calculate factorial of 20 using Python",

        "Read a CSV using pandas",

        "Plot a sine wave using matplotlib",

        "Generate Python code to print primes",

    ]

    for test in tests:

        print(test)

        print("→", router.detect(test))

        print()