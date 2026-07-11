"""
Athena AI - Conversation Service

Responsible for:

- Active conversation management
- Loading history
- Saving messages
- Searching conversations
- Rename
- Pin
- Folder management
- Prompt history building

UI never directly touches storage.
"""

from app.settings import settings
from app.conversation_store import ConversationStore
from app.title_generator import generate_title


class ConversationService:


    def __init__(self):

        self.store = ConversationStore()

        conversations = self.store.list()


        if conversations:

            self.active_conversation = (
                self.store.load(
                    conversations[0]["id"]
                )
            )

        else:

            self.active_conversation = (
                self.store.create()
            )



    # =====================================================
    # Active Conversation
    # =====================================================


    def get_active_conversation(self):

        return self.active_conversation



    def new_conversation(self):

        self.active_conversation = (
            self.store.create()
        )

        return self.active_conversation



    def switch_conversation(
        self,
        conversation_id
    ):


        conversation = (
            self.store.load(
                conversation_id
            )
        )


        if conversation:

            self.active_conversation = conversation


        return self.active_conversation



    # =====================================================
    # Listing / Searching
    # =====================================================


    def list_conversations(self):

        return self.store.list()



    def search_conversations(
        self,
        query
    ):

        return self.store.search(
            query
        )



    # =====================================================
    # History
    # =====================================================


    def load_history(
        self,
        user_name=None
    ):

        if not self.active_conversation:

            return []


        limit = (
            settings.get_history()
        )


        return (
            self.active_conversation
            .messages[-limit:]
        )



    def format_history(
        self,
        history
    ):


        return "\n".join(

            f"{msg['role']}: {msg['content']}"

            for msg in history

        )



    # =====================================================
    # Message Saving
    # =====================================================


    def save_user_message(
        self,
        user_name,
        message
    ):


        self.active_conversation.messages.append({

            "role":
                "User",

            "content":
                message

        })



        # Auto title generation

        if (

            self.active_conversation.title
            == "New Chat"

            and

            len(
                self.active_conversation.messages
            )
            == 1

        ):


            self.active_conversation.title = (
                generate_title(
                    message
                )
            )



        self.store.save(
            self.active_conversation
        )



    def save_ai_message(
        self,
        user_name,
        message
    ):


        self.active_conversation.messages.append({

            "role":
                "Athena",

            "content":
                message

        })


        self.store.save(
            self.active_conversation
        )



    # =====================================================
    # Rename
    # =====================================================


    def rename_conversation(
        self,
        conversation_id,
        title
    ):


        conversation = (
            self.store.load(
                conversation_id
            )
        )


        if conversation:


            conversation.title = title

            self.store.save(
                conversation
            )


        return conversation



    # =====================================================
    # Delete
    # =====================================================


    def delete_conversation(
        self,
        conversation_id
    ):


        self.store.delete(
            conversation_id
        )


        remaining = (
            self.store.list()
        )


        if remaining:


            self.active_conversation = (
                self.store.load(
                    remaining[0]["id"]
                )
            )

        else:


            self.active_conversation = (
                self.store.create()
            )



    # =====================================================
    # Pin
    # =====================================================


    def pin_conversation(
        self,
        conversation_id
    ):

        self.store.set_pin(
            conversation_id,
            True
        )



    def unpin_conversation(
        self,
        conversation_id
    ):

        self.store.set_pin(
            conversation_id,
            False
        )



    # =====================================================
    # Folder
    # =====================================================


    def move_to_folder(
        self,
        conversation_id,
        folder
    ):


        self.store.set_folder(
            conversation_id,
            folder
        )



    # =====================================================
    # Document Prompt
    # =====================================================


    def build_document_prompt(
        self,
        user_name,
        message,
        document_text,
        file_name="document"
    ):


        system_prompt = (
            self.load_system_prompt()
        )


        history = (
            self.load_history(
                user_name
            )
        )


        conversation = (
            self.format_history(
                history
            )
        )


        return f"""
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



    # =====================================================
    # System Prompt
    # =====================================================


    def load_system_prompt(self):

        with open(
            "prompts/system_prompt.txt",
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()



conversation_service = ConversationService()