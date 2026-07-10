from services.prompt_builders.chat_prompt_builder import (
    chat_prompt_builder
)

prompt = chat_prompt_builder.build(
    user_name="User",
    message="Hello Athena!"
)

print(prompt)