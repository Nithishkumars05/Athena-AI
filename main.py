from agents.chat_agent import chat
from agents.report_agent import create_report


print("=" * 60)
print("               ATHENA AI v4.0")
print("=" * 60)

name = input("Enter your name: ")

print(f"\nWelcome {name}!")
print("Commands:")
print(" - Chat normally")
print(" - generate report on <topic>")
print(" - exit\n")


while True:

    user = input(f"{name}: ")

    if user.lower() == "exit":
        print("\nAthena: Goodbye! Have a wonderful day.")
        break
    if user.lower().startswith("generate report on"):
        topic=user[18:].strip()
        print("\nAthena : Generating report ...\n")
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
        report=chat(name,prompt)
        filename=create_report(topic,report)
        print(f"\nAthena : Report generated successfully !!")
        print(f"Saved as : {filename}")
        print("-"*60)
    else:
        answer=chat(name,user)
        print("\nAthena :",answer)
        print("-"*60)

    