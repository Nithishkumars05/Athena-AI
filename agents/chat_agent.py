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
from core.routers.task_router import task_router
from core.routers.model_router import model_router

def chat(user_name: str, message: str) -> str:

    task_type = task_router.classify(message)

    model_name = model_router.select_model(
        task_type
    )

    return model_manager.generate_with_model(
        model_name=model_name,
        user_name=user_name,
        message=message
    )
def handle(user_name: str, message: str) -> str:
    return chat(user_name, message)

def stream(user_name: str, message: str):

    task_type = task_router.classify(message)

    model_name = model_router.select_model(
        task_type
    )

    yield from model_manager.stream_generate_with_model(
        model_name=model_name,
        user_name=user_name,
        message=message
    )


def stream_handle(user_name: str, message: str):

    yield from stream(
        user_name,
        message
    )