from services.prompt_builders.document_prompt_builder import (
    document_prompt_builder
)

prompt = document_prompt_builder.build(
    user_name="User",
    message="Summarize this document.",
    document_text="Athena AI is a modular desktop assistant.",
    file_name="sample.docx"
)

print(prompt)