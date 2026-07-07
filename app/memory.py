"""
Athena AI Memory Service (In-Memory)

Future upgrade:
- SQLite
- ChromaDB
- PostgreSQL
- Vector Database

API:
    add_message(user_name, role, content)
    get_history(user_name)
    clear_history(user_name=None)
"""

from collections import defaultdict

# Stores conversations per user
_memory = defaultdict(list)


def add_message(user_name: str, role: str, content: str):
    """
    Store a message for a user.

    Example:
    {
        "role": "User",
        "content": "Hello"
    }
    """

    _memory[user_name].append({
        "role": role,
        "content": content
    })


def get_history(user_name: str):
    """
    Returns conversation history for one user.

    Returns:
    [
        {"role": "User", "content": "..."},
        {"role": "Athena", "content": "..."}
    ]
    """

    return _memory[user_name]


def clear_history(user_name: str = None):
    """
    Clear memory.

    If user_name is None:
        Clears everyone's memory.

    Else:
        Clears only that user's conversation.
    """

    if user_name is None:
        _memory.clear()
    else:
        _memory[user_name].clear()