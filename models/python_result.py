"""
Athena AI

Python Result Model

Represents the result of Python code execution.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class PythonResult:
    """
    Result returned by the Python execution engine.
    """

    success: bool

    stdout: str = ""

    stderr: str = ""

    execution_time: float = 0.0

    exit_code: int = 0

    generated_file: Optional[str] = None