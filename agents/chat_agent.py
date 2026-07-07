"""
Athena AI - Chat Agent

The Chat Agent acts as a coordinator.
It does not know which AI model is being used.

Flow:
UI
 ↓
ChatService
 ↓
ChatWorker
 ↓
ChatAgent
 ↓
ModelManager
 ↓
Gemini / OpenAI / Ollama
"""

from core.model_manager import model_manager


def chat(user_name: str, message: str) -> str:
    """
    Delegate the chat request to the currently
    selected AI model.

    Args:
        user_name: Name of the current user.
        message: User's input message.

    Returns:
        AI-generated response.
    """

    return model_manager.generate(
        user_name=user_name,
        message=message
    )