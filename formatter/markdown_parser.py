import re


def add_markdown_runs(paragraph, text):
    """
    Convert **bold** markdown into Word bold formatting.
    """

    parts = re.split(r"(\*\*.*?\*\*)", text)

    for part in parts:

        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True

        else:
            paragraph.add_run(part)