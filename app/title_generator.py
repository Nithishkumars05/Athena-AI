import re


def generate_title(message: str):

    if not message:
        return "New Chat"


    # Remove special characters

    cleaned = re.sub(
        r"[^a-zA-Z0-9 ]",
        "",
        message
    )


    words = cleaned.split()


    if len(words) <= 5:

        title = " ".join(words)

    else:

        title = " ".join(
            words[:5]
        )


    return title.title()