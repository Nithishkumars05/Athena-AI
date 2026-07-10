from models.chat_request import ChatRequest
from services.request_processor import request_processor

request = ChatRequest(
    user_name="User",
    message="Hello Athena!"
)

processed = request_processor.process(request)

print(processed)