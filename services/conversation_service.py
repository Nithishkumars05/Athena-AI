"""
Athena AI - Conversation Service

Responsible for:

- Loading system prompt
- Loading conversation history
- Saving messages
- Building prompts

Every AI model should use this service.
"""

from app.settings import settings
from app.conversation_store import ConversationStore


class ConversationService:

    def __init__(self):
        self.store = ConversationStore()

        conversations = self.store.list()

        if conversations:
            self.active_conversation = self.store.load(
                conversations[0]["id"]
            )
        else:
            self.active_conversation = self.store.create()

        

    def get_active_conversation(self):
        return self.active_conversation


    def new_conversation(self):
        self.active_conversation = self.store.create()
        return self.active_conversation


    def switch_conversation(self, conversation_id):


        conversation = self.store.load(
        conversation_id
    )

        if conversation:

            self.active_conversation = conversation

        return self.active_conversation
    def list_conversations(self):
        return self.store.list()

    def load_history(self, user_name=None):

        history_limit = settings.get_history()

        return self.active_conversation.messages[-history_limit:]

    def format_history(self, history):

        return "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in history
        )

    def save_user_message(self, user_name, message):

        self.active_conversation.messages.append(
        {
            "role": "User",
            "content": message
        }
    )

        self.store.save(self.active_conversation)

    def rename_conversation(self, conversation_id, title):

        conversation = self.store.load(
        conversation_id
    )

        if conversation:

            conversation.title = title

            self.store.save(
            conversation
        )

        return conversation


    def delete_active_conversation(self):

        conversation_id = self.active_conversation.id

        self.store.delete(conversation_id)

        conversations = self.store.list()

        if conversations:
            self.active_conversation = self.store.load(
                conversations[0]["id"]
        )
        else:
            self.active_conversation = self.store.create()

    def delete_conversation(self, conversation_id):

        self.store.delete(
        conversation_id
    )


        conversations = self.store.list()


        if conversations:

            self.active_conversation = self.store.load(
            conversations[0]["id"]
        )

        else:

            self.active_conversation = self.store.create()
    
    def build_document_prompt(
        self,
        user_name: str,
        message: str,
        document_text: str,
        file_name: str = "document"
    ):
        """
        Build a prompt that includes uploaded document content.
        """

        system_prompt = self.load_system_prompt()

        history = self.load_history(user_name)
        conversation = self.format_history(history)

        prompt = f"""
{system_prompt}

Conversation:
{conversation}

Uploaded File:
{file_name}

Document Content:
----------------
{document_text}
----------------

User Request:
{message}

Athena:
"""

        return prompt

    def load_system_prompt(self):

        with open(
        "prompts/system_prompt.txt",
        "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    def save_ai_message(self, user_name, message):

        self.active_conversation.messages.append(
        {
            "role": "Athena",
            "content": message
        }
    )

        self.store.save(self.active_conversation)


conversation_service = ConversationService()