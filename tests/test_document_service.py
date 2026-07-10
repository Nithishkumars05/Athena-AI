from services.document_service import document_service

try:
    prompt = document_service.build_prompt(
        user_name="User",
        message="Summarize this document.",
        file_path="sample.docx"
    )

    print("========== PROMPT ==========")
    print(prompt)

except Exception as e:
    print(type(e).__name__)
    print(e)