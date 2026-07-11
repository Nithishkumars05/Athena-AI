import json
import uuid
from pathlib import Path
from datetime import datetime

from models.conversation import Conversation


class ConversationStore:
    """
    Handles persistent storage for conversations.

    memory/
        conversations/
            <conversation_id>.json
        index.json
    """

    def __init__(self, memory_dir="memory"):
        self.memory_dir = Path(memory_dir)
        self.conversations_dir = self.memory_dir / "conversations"

        self.memory_dir.mkdir(exist_ok=True)
        self.conversations_dir.mkdir(exist_ok=True)

        self.index_file = self.memory_dir / "index.json"

        if not self.index_file.exists():
            self.index_file.write_text("[]", encoding="utf-8")

    # ---------------------------------------------------------

    def _load_index(self):
        with open(self.index_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_index(self, index):
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4,ensure_ascii=False,)

    # ---------------------------------------------------------

    def create(self, title="New Chat") -> Conversation:

        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=title
        )

        self.save(conversation)

        index = self._load_index()

        index.append({
            "id": conversation.id,
            "title": conversation.title,
            "updated_at": conversation.updated_at
        })

        self._save_index(index)

        return conversation

    # ---------------------------------------------------------

    def save(self, conversation: Conversation):

        conversation.updated_at = datetime.now().isoformat()

        path = self.conversations_dir / f"{conversation.id}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(conversation.__dict__, f, indent=4)

        index = self._load_index()

        for item in index:
            if item["id"] == conversation.id:
                item["title"] = conversation.title
                item["updated_at"] = conversation.updated_at
                break

        self._save_index(index)

    # ---------------------------------------------------------

    def load(self, conversation_id: str) -> Conversation | None:

        path = self.conversations_dir / f"{conversation_id}.json"

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Conversation(**data)

    # ---------------------------------------------------------

    def delete(self, conversation_id: str):

        path = self.conversations_dir / f"{conversation_id}.json"

        if path.exists():
            path.unlink()

        index = [
            item for item in self._load_index()
            if item["id"] != conversation_id
        ]

        self._save_index(index)

    # ---------------------------------------------------------

    def rename(self, conversation_id: str, new_title: str):

        conversation = self.load(conversation_id)

        if conversation is None:
            return

        conversation.title = new_title
        self.save(conversation)

    # ---------------------------------------------------------

    def list(self):

        index = self._load_index()

        return sorted(
            index,
            key=lambda x: x["updated_at"],
            reverse=True
        )
    
    def search(self, query: str):

        query = query.lower().strip()

        if not query:
            return self.list()

        results = []

        for item in self.list():

            conversation = self.load(item["id"])

            if conversation is None:
                continue

        # Search title
            if query in conversation.title.lower():
                results.append(item)
                continue

        # Search messages
            for message in conversation.messages:

                if query in message["content"].lower():

                    results.append(item)
                    break

        return results