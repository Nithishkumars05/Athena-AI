from pypdf import PdfReader
from docx import Document

from agents.chat_agent import chat


def read_document(file_path):
    """
    Reads TXT, PDF, and DOCX files and returns their text.
    """

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return text

    elif file_path.endswith(".docx"):
        doc = Document(file_path)

        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text

    else:
        raise ValueError("Unsupported file type.")


def summarize_document(user_name, file_path):
    text = read_document(file_path)

    prompt = f"""
Summarize the following document.

Document:

{text}
"""

    return chat(user_name, prompt)