from core.routers.task_router import task_router


tests = [
    "Write a Python function",
    "Explain quantum physics deeply",
    "Summarize this PDF",
    "Calculate 25*30",
    "Tell me a joke"
]


for t in tests:
    print(t)
    print("→", task_router.classify(t))
    print()