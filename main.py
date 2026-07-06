from agents.document_agent import summarize_document
from agents.chat_agent import chat
from agents.report_agent import create_report


# ---------------------------
# ATHENA UI HEADER
# ---------------------------
print("=" * 60)
print("               ATHENA AI v4.0")
print("=" * 60)

name = input("Enter your name: ").strip()

print(f"\nWelcome {name}!\n")


# ---------------------------
# COMMAND SYSTEM
# ---------------------------
COMMANDS = {
    "chat": ["chat", "c"],
    "report": ["report", "r"],
    "summarize": ["summarize", "s", "sum"],
    "help": ["help", "h"],
    "exit": ["exit", "q", "quit"]
}


def normalize_command(user_input):
    user_input = user_input.lower().strip()

    for cmd, aliases in COMMANDS.items():
        if user_input in aliases:
            return cmd

    return None


def show_help():
    print("""
================ HELP MENU ================
chat (c)        → Talk with Athena
report (r)      → Generate AI report
summarize (s)   → Summarize a document
help (h)        → Show this menu
exit (q)        → Quit Athena
==========================================
""")


def generate_report_flow(name):
    topic = input("\nEnter report topic: ").strip()

    print("\nAthena: Generating report...\n")

    prompt = f"""
Write a detailed report on:

{topic}

Include:
1. Introduction
2. Explanation
3. Advantages
4. Disadvantages
5. Applications
6. Conclusion
"""

    report = chat(name, prompt)
    filename = create_report(topic, report)

    print("\nAthena: Report generated successfully!!")
    print(f"Saved as: {filename}")
    print("-" * 60)


def summarize_flow(name):
    file_path = input("\nEnter document path: ").strip().strip('"')

    try:
        print("\nAthena: Reading document...\n")

        summary = summarize_document(name, file_path)

        print("\nAthena Summary:\n")
        print(summary)
        print("-" * 60)

    except Exception as e:
        if "429" in str(e):
            print("\nAthena: API quota exceeded. Please wait or try again later.")
        else:
            print(f"\nError: {e}")


# ---------------------------
# MAIN LOOP
# ---------------------------
while True:
    user_input = input(f"{name}: ").strip()

    cmd = normalize_command(user_input)

    # ---------------- CHAT ----------------
    if cmd == "chat" or cmd is None:
        # If user didn't type a command → treat as chat
        answer = chat(name, user_input)
        print("\nAthena:", answer)
        print("-" * 60)

    # ---------------- REPORT ----------------
    elif cmd == "report":
        generate_report_flow(name)

    # ---------------- SUMMARIZE ----------------
    elif cmd == "summarize":
        summarize_flow(name)

    # ---------------- HELP ----------------
    elif cmd == "help":
        show_help()

    # ---------------- EXIT ----------------
    elif cmd == "exit":
        print("\nAthena: Goodbye! Have a wonderful day 👋")
        break

    else:
        print("\nAthena: Invalid command. Type 'help' for options.")