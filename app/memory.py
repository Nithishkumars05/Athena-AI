chat_history=[]

def add_message(role,message):
    chat_history.append(f"{role} : {message}")
def get_history():
    return "\n".join(chat_history)
def clear_history():
    chat_history.clear()