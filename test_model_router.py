from core.routers.model_router import model_router
from core.enums.task_type import TaskType


tests = [
    TaskType.CODING,
    TaskType.REASONING,
    TaskType.VISION,
    TaskType.MATH,
    TaskType.CHAT
]


for task in tests:

    print(task)

    print(
        "→",
        model_router.select_model(task)
    )

    print()