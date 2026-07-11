from core.conversation_manager import conversation_manager
from services.processors.context_builder import context_builder
conversation_manager.new_conversation()

conversation_manager.add_message("user", "Hello")
conversation_manager.add_message("assistant", "Hi!")

prompt = context_builder.build("Tell me about Python")

print(prompt)