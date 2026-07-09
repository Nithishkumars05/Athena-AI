from agents.chat_agent import chat


tests = [
    "Write a Python function to reverse a list",
    "Explain why black holes form",
    "Tell me a joke"
]


for t in tests:

    print("\nUSER:")
    print(t)

    print("\nATHENA:")
    print(
        chat(
            "Nithish",
            t
        )
    )