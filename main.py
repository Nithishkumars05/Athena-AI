from agents.document_agent import summarize_document
from agents.chat_agent import chat
from agents.report_agent import create_report
from agents.intent_router import router
from agents.math_agent import (
    solve_equation,
    simplify_expression,
    differentiate_expression,
    integrate_expression,
    factor_expression,
    expand_expression,
)
from formatter.math_formatter import format_math


# ==========================================================
# ATHENA AI v4.1
# ==========================================================

print("=" * 60)
print("               ATHENA AI v4.1")
print("=" * 60)

name = input("Enter your name: ").strip()

print(f"\nWelcome {name}!\n")


# ==========================================================
# COMMANDS
# ==========================================================

COMMANDS = {
    "chat": ["chat", "c"],
    "report": ["report", "r"],
    "summarize": ["summarize", "s", "sum"],
    "help": ["help", "h"],
    "exit": ["exit", "q", "quit"],
}


def normalize_command(user_input):
    user_input = user_input.lower().strip()

    for cmd, aliases in COMMANDS.items():
        if user_input in aliases:
            return cmd

    return None


# ==========================================================
# OUTPUT
# ==========================================================

def athena_print(text):
    text = format_math(str(text))
    print(f"\nAthena: {text}")
    print("-" * 60)


# ==========================================================
# HELP
# ==========================================================

def show_help():
    print("""
================= ATHENA HELP =================

chat (c)
    Talk with Athena

report (r)
    Generate a report

summarize (s)
    Summarize a document

Math Examples:
    solve x**2 + 5*x + 6
    simplify (x**2-1)/(x-1)
    differentiate x**3 + 4*x
    integrate x**2
    factor x**2+5*x+6
    expand (x+2)**3

help (h)
    Show help

exit (q)
    Quit Athena

===============================================
""")


# ==========================================================
# REPORT
# ==========================================================

def generate_report_flow(name):

    topic = input("\nEnter report topic: ").strip()

    athena_print("Generating report...")

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
    report = format_math(report)

    filename = create_report(topic, report)

    athena_print("Report generated successfully.")
    print("Saved as:", filename)
    print("-" * 60)


# ==========================================================
# SUMMARIZER
# ==========================================================

def summarize_flow(name):

    file_path = input("\nEnter document path: ").strip().strip('"')

    try:

        athena_print("Reading document...")

        summary = summarize_document(name, file_path)

        print("\nAthena Summary:\n")
        print(format_math(summary))
        print("-" * 60)

    except Exception as e:

        if "429" in str(e):
            athena_print("API quota exceeded. Please try again later.")

        else:
            athena_print(e)


# ==========================================================
# MATH AGENT
# ==========================================================

def math_flow(user_input):

    text = user_input.lower()

    try:

        if text.startswith("solve"):
            expression = user_input[5:].strip()
            return solve_equation(expression)

        elif text.startswith("simplify"):
            expression = user_input[8:].strip()
            return simplify_expression(expression)

        elif text.startswith("differentiate"):
            expression = user_input[13:].strip()
            return differentiate_expression(expression)

        elif text.startswith("integrate"):
            expression = user_input[9:].strip()
            return integrate_expression(expression)

        elif text.startswith("factor"):
            expression = user_input[6:].strip()
            return factor_expression(expression)

        elif text.startswith("expand"):
            expression = user_input[6:].strip()
            return expand_expression(expression)

        return "Unknown mathematical command."

    except Exception as e:
        return f"Math Error: {e}"


# ==========================================================
# MAIN LOOP
# ==========================================================

while True:

    user_input = input(f"{name}: ").strip()

    if not user_input:
        continue

    cmd = normalize_command(user_input)
    intent = router.detect(user_input)

    # ---------------- EXIT ----------------
    if cmd == "exit":
        athena_print("Goodbye! Have a wonderful day 👋")
        break

    # ---------------- HELP ----------------
    elif cmd == "help":
        show_help()

    # ---------------- REPORT ----------------
    elif cmd == "report":
        generate_report_flow(name)

    # ---------------- SUMMARIZE ----------------
    elif cmd == "summarize":
        summarize_flow(name)

    # ---------------- MATH ----------------
    elif intent == "math":
        result = math_flow(user_input)
        athena_print(result)

    # ---------------- CHAT ----------------
    else:
        try:
            answer = chat(name, user_input)
            athena_print(answer)

        except Exception as e:

            if "429" in str(e):
                athena_print("API quota exceeded. Chat is temporarily unavailable.")
            else:
                athena_print(e)