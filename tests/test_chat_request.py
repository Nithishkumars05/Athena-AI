from models.chat_request import ChatRequest

request = ChatRequest(
    user_name="User",
    message="Summarize this document.",
    file_path="sample.docx"
)

print(request)