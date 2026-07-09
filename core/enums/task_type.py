from enum import Enum


class TaskType(Enum):
    """
    Represents the type of task Athena needs to perform.
    """

    CHAT = "chat"

    CODING = "coding"

    REASONING = "reasoning"

    VISION = "vision"

    DOCUMENT = "document"

    MATH = "math"