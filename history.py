import json
import os

HISTORY_FILE = "chat_history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    with open(HISTORY_FILE, "w") as file:
        json.dump([], file, indent=4)

    return []


def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def show_history(history):
    print("\n📜 Conversation History")
    print("----------------------------")

    if not history:
        print("No conversation yet.\n")
        return

    for message in history:
        print(f"{message['role'].capitalize()}: {message['content']}")

    print()