"""
Athena AI - Conversation Memory

Handles persistent storage of conversations.
"""

import json
from pathlib import Path


class ConversationMemory:

    def __init__(self):

        self.storage_path = Path(
            "memory/conversations"
        )

        self.storage_path.mkdir(
            parents=True,
            exist_ok=True
        )


    def save(self, conversation):

        conversation_id = conversation.id

        file_path = self.storage_path / f"{conversation_id}.json"

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                conversation.to_dict(),
                file,
                indent=4,
                ensure_ascii=False
            )


    def load(self, conversation_id):

        file_path = self.storage_path / f"{conversation_id}.json"

        if not file_path.exists():
            return None

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


conversation_memory = ConversationMemory()