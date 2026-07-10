from app.conversation_store import ConversationStore

print("=" * 50)
print("Creating ConversationStore...")
print("=" * 50)

store = ConversationStore()

print("\nCreating a new conversation...")

conversation = store.create("Testing Conversation")

print(f"Conversation ID: {conversation.id}")
print(f"Title: {conversation.title}")

print("\nLoading conversation...")

loaded = store.load(conversation.id)

print(f"Loaded Title: {loaded.title}")

print("\nAdding messages...")

loaded.messages.append(
    {
        "role": "user",
        "content": "Hello Athena!"
    }
)

loaded.messages.append(
    {
        "role": "assistant",
        "content": "Hello! How can I help?"
    }
)

store.save(loaded)

print("Messages saved.")

print("\nListing conversations...")

for item in store.list():
    print(item)

print("\nRenaming conversation...")

store.rename(conversation.id, "Python Testing")

renamed = store.load(conversation.id)

print("New title:", renamed.title)

print("\nDeleting conversation...")

store.delete(conversation.id)

print("\nRemaining conversations:")

print(store.list())

print("\nAll tests finished.")