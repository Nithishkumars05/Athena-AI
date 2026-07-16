from models.chat_request import ChatRequest
from agents.python_agent import handle


request = ChatRequest(
    user_name="Nithish",
    message="Write Python code to print the first 10 Fibonacci numbers.",
    conversation_id=None,
    file_path=None,
)

print(handle(request))