from app.config import client
from app.memory import add_message, get_history


def format_history(history):
    """
    Converts memory into clean LLM-friendly format
    """
    return "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in history]
    )


def chat(user_name: str, user_input: str) -> str:
    # 1. Save user message
    add_message(user_name, "User", user_input)

    # 2. Load system prompt
    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 3. Get last messages (memory control)
    history = get_history(user_name)[-20:]

    # 4. Format conversation
    conversation_text = format_history(history)

    # 5. Build final prompt
    prompt = f"""
{system_prompt}

Conversation:
{conversation_text}

User: {user_input}
Athena:
"""

    # 6. Call Gemini model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if hasattr(response, "text") and response.text:
        answer = response.text.strip()
    else:
        answer = "Sorry, I couldn't generate a response."

    # 7. Save Athena response
    add_message(user_name, "Athena", answer)

    return answer