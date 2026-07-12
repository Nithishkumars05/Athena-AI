import json
import uuid

from pathlib import Path
from datetime import datetime

from models.conversation import Conversation



class ConversationStore:
    """
    Athena AI Conversation Storage

    Handles:

    - Creating conversations
    - Saving conversations
    - Loading conversations
    - Searching
    - Deleting
    - Metadata management


    Storage:

    memory/
        conversations/
            <id>.json

        index.json

    """


    def __init__(
        self,
        memory_dir="memory"
    ):

        self.memory_dir = Path(
            memory_dir
        )

        self.conversations_dir = (
            self.memory_dir /
            "conversations"
        )


        self.memory_dir.mkdir(
            exist_ok=True
        )


        self.conversations_dir.mkdir(
            exist_ok=True
        )


        self.index_file = (
            self.memory_dir /
            "index.json"
        )


        if not self.index_file.exists():

            self.index_file.write_text(
                "[]",
                encoding="utf-8"
            )



    # =====================================================
    # Index Handling
    # =====================================================


    def _load_index(self):

        try:

            with open(
                self.index_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)


        except:

            return []



    def _save_index(
        self,
        index
    ):

        with open(
            self.index_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                index,
                f,
                indent=4,
                ensure_ascii=False
            )



    # =====================================================
    # Create
    # =====================================================


    # =====================================================
# Create
# =====================================================

    def create(
    self,
    title="New Chat"
):

        conversation = Conversation(
        id=str(uuid.uuid4()),
        title=title,
        pinned=False,
        folder="General"
    )

        self.save(conversation)

        return conversation
    # =====================================================
    # Save
    # =====================================================


    def save(
        self,
        conversation
    ):


        conversation.updated_at = datetime.now().isoformat()


        path = (
            self.conversations_dir /
            f"{conversation.id}.json"
        )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                conversation.__dict__,
                f,
                indent=4,
                ensure_ascii=False
            )



        index = self._load_index()


        found = False


        for item in index:


            if item["id"] == conversation.id:


                item.update({

                    "title":
                        conversation.title,

                    "updated_at":
                        conversation.updated_at,

                    "pinned":
                        conversation.pinned,

                    "folder":
                        conversation.folder

                })


                found = True
                break



        if not found:


            index.append({

                "id":
                    conversation.id,

                "title":
                    conversation.title,

                "updated_at":
                    conversation.updated_at,

                "pinned":
                    conversation.pinned,

                "folder":
                    conversation.folder

            })



        self._save_index(
            index
        )



    # =====================================================
    # Load
    # =====================================================


    def load(
        self,
        conversation_id
    ):


        path = (
            self.conversations_dir /
            f"{conversation_id}.json"
        )


        if not path.exists():

            return None



        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)



        # Migration support

        data.setdefault(
            "pinned",
            False
        )

        data.setdefault(
            "folder",
            "General"
        )
        data.setdefault(
    "archived",
    False
)

        data.setdefault(
    "deleted",
    False
)

        data.setdefault(
    "tags",
    []
)

        


        return Conversation(
            **data
        )



    # =====================================================
    # Delete
    # =====================================================


    def delete(
        self,
        conversation_id
    ):


        path = (
            self.conversations_dir /
            f"{conversation_id}.json"
        )


        if path.exists():

            path.unlink()



        index = [

            item

            for item in self._load_index()

            if item["id"] != conversation_id

        ]


        self._save_index(
            index
        )



    # =====================================================
    # Rename
    # =====================================================


    def rename(
        self,
        conversation_id,
        title
    ):


        conversation = self.load(
            conversation_id
        )


        if conversation:


            conversation.title = title

            self.save(
                conversation
            )



    # =====================================================
    # List
    # =====================================================


    def list(self):


        conversations = (
            self._load_index()
        )


        return sorted(

            conversations,

            key=lambda x:
                (
                    x.get(
                        "pinned",
                        False
                    ),

                    x.get(
                        "updated_at",
                        ""
                    )

                ),

            reverse=True

        )



    # =====================================================
    # Search
    # =====================================================


    def search(
        self,
        query
    ):


        query = (
            query
            .lower()
            .strip()
        )


        if not query:

            return self.list()



        results = []


        for item in self.list():


            conversation = self.load(
                item["id"]
            )


            if not conversation:

                continue



            if query in conversation.title.lower():

                results.append(item)

                continue



            for message in conversation.messages:


                content = message.get(
                    "content",
                    ""
                ).lower()


                if query in content:

                    results.append(item)

                    break



        return results



    # =====================================================
    # Metadata
    # =====================================================


    def set_pin(
        self,
        conversation_id,
        value=True
    ):


        conversation = self.load(
            conversation_id
        )


        if conversation:

            conversation.pinned = value

            self.save(
                conversation
            )



    def set_folder(
        self,
        conversation_id,
        folder
    ):


        conversation = self.load(
            conversation_id
        )


        if conversation:

            conversation.folder = folder

            self.save(
                conversation
            )