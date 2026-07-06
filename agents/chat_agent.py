from app.config import client
from app.memory import add_message,get_history
 
def chat(user_name,user_input):
    add_message(user_name,user_input)
    with open("prompts/system_prompt.txt","r",encoding="utf-8") as f:
        system_prompt=f.read()

    prompt=f"""
{system_prompt}

Conversation :
{get_history()}

Athena :
"""
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    answer=response.text
    add_message("Athena",answer)
    return answer
