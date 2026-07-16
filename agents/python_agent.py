"""
Athena AI

Python Agent

Responsibilities
----------------
- Ask the AI to generate Python code
- Execute the generated code
- Return formatted results

Future:
- Multiple execution rounds
- Auto bug fixing
- File generation
- Graph generation
- Package management
"""

from models.chat_request import ChatRequest

from agents.chat_agent import chat
from services.python_executor import python_executor


SYSTEM_PROMPT = """
You are an expert Python programmer.

Generate ONLY executable Python code.

Rules:
- Do NOT use markdown.
- Do NOT wrap code inside ```python.
- Do NOT explain the code.
- Do NOT print unnecessary text.
- Use only Python.
- Produce clean executable code.
"""


def handle(request: ChatRequest) -> str:
    """
    Generates Python code using the LLM,
    executes it, and returns the result.
    """

    prompt = f"""{SYSTEM_PROMPT}

Task:

{request.message}
"""

    python_request = ChatRequest(
        user_name=request.user_name,
        message=prompt,
        conversation_id=request.conversation_id,
        file_path=None,
    )

    code = chat(python_request).strip()

    # Remove accidental markdown fences
    if code.startswith("```"):
        lines = code.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        code = "\n".join(lines)

    result = python_executor.execute(code)

    response = []

    response.append("# Python Execution")

    response.append("")

    response.append("## Generated Code")

    response.append("```python")
    response.append(code)
    response.append("```")

    response.append("")

    if result.success:

        response.append("## Output")

        response.append("```text")
        response.append(result.stdout or "(No Output)")
        response.append("```")

    else:

        response.append("## Error")

        response.append("```text")
        response.append(result.stderr)
        response.append("```")

    response.append("")

    response.append(
        f"Execution Time: {result.execution_time:.3f} sec"
    )

    return "\n".join(response)