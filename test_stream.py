from agents.chat_agent import stream


for chunk in stream(
    "Nithish",
    "Tell me a short story"
):
    print(chunk, end="", flush=True)