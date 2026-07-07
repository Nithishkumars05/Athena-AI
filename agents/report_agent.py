"""
Athena AI - Report Agent

Flow:
Dispatcher
    ↓
Report Agent
    ↓
Chat Agent (Gemini/OpenAI/Ollama)
    ↓
Report Generator
    ↓
DOCX Report
"""

import re

from agents.chat_agent import chat
from formatter.report_generator import create_report


def handle(user_name: str, message: str) -> str:
    """
    Handles report generation requests.
    """

    topic = extract_topic(message)

    prompt = f"""
Write a professional, detailed report on the following topic.

Topic:
{topic}

Use proper markdown formatting.

Include:

# Title

## Introduction

## Main Concepts

## Applications

## Advantages

## Challenges

## Future Scope

## Conclusion
"""

    content = chat(user_name, prompt)

    filename = create_report(topic, content)

    return (
        f"✅ Report generated successfully!\n\n"
        f"Saved to:\n{filename}"
    )


def extract_topic(message: str) -> str:
    """
    Extract report topic from user request.
    """

    message = message.lower().strip()

    patterns = [
        r"generate report on",
        r"create report on",
        r"write report on",
        r"report on",
    ]

    topic = message

    for pattern in patterns:
        topic = re.sub(pattern, "", topic)

    topic = topic.strip()

    if not topic:
        topic = "Untitled Report"

    return topic