from google import genai
from dotenv import load_dotenv
import os
import json

from config import (
    MAX_HISTORY,
    SUMMARY_TRIGGER,
    EXIT_COMMANDS,
)

from utils import (
    clear_screen,
    show_help,
    show_time,
)

from history import (
    load_history,
    save_history,
    show_history,
)

from memory import (
    load_memory,
    save_memory,
    update_memory,
)

from summary import (
    load_summary,
    save_summary,
)

from prompts import (
    build_chat_prompt,
    build_memory_prompt,
    build_summary_prompt,
)


# ==========================================
# Load Environment Variables
# ==========================================
load_dotenv()


# ==========================================
# Gemini Client
# ==========================================
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chat = client.chats.create(
    model="gemini-2.5-flash-lite"
)


print("🤖 Welcome to NovaMind!")
print("Type 'help' to see available commands.\n")


# ==========================================
# Counters
# ==========================================
user_messages = 0
ai_requests = 0


# ==========================================
# Load Stored Data
# ==========================================
history = load_history()
memory = load_memory()
conversation_summary = load_summary()


# ==========================================
# Summarize Old Conversations
# ==========================================
if len(history) > SUMMARY_TRIGGER:

    old_messages = history[:-MAX_HISTORY]

    old_context = ""

    for msg in old_messages:
        old_context += f"{msg['role']}: {msg['content']}\n"

    summary_prompt = build_summary_prompt(
        conversation_summary,
        old_context,
    )

    summary_response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=summary_prompt,
    )

    conversation_summary = summary_response.text

    save_summary(conversation_summary)

    history = history[-MAX_HISTORY:]
    save_history(history)

    print("📝 Conversation summarized successfully!")


# ==========================================
# Main Chat Loop
# ==========================================
while True:

    question = input("You: ").strip()

    if not question:
        print("⚠️ Please enter a message.\n")
        continue

    command = question.lower()

    # ======================================
    # Exit
    # ======================================
    if command in EXIT_COMMANDS:

        print("\n📊 Session Summary")
        print(f"Total Messages : {user_messages}")
        print(f"AI Requests    : {ai_requests}")
        print("👋 Goodbye!")

        break

    user_messages += 1

    # ======================================
    # Commands
    # ======================================
    if command == "help":
        show_help()
        continue

    elif command == "hello":
        print("\n🤖 Hello Tejasri! 😊\n")
        continue

    elif command == "time":
        show_time()
        continue

    elif command == "clear":
        clear_screen()
        continue

    elif command == "history":
        show_history(history)
        continue

    # ======================================
    # Store User Message
    # ======================================
    history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # ======================================
    # Build Prompt
    # ======================================
    big_prompt = build_chat_prompt(
        memory,
        conversation_summary,
        history,
        question,
    )

    try:

        # ==================================
        # Ask Gemini
        # ==================================
        response = chat.send_message(big_prompt)

        ai_requests += 1

        print(f"\n🤖 NovaMind: {response.text}\n")

        # ==================================
        # Save AI Response
        # ==================================
        history.append(
            {
                "role": "assistant",
                "content": response.text,
            }
        )

        # ==================================
        # Extract Long-Term Memory
        # ==================================
        memory_prompt = build_memory_prompt(
            memory,
            question,
            response.text,
        )

        memory_response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=memory_prompt,
        )

        memory_text = memory_response.text.strip()

        # ==================================
        # Remove Markdown Code Blocks
        # ==================================
        if memory_text.startswith("```json"):
            memory_text = memory_text.replace(
                "```json",
                "",
                1,
            )

        if memory_text.endswith("```"):
            memory_text = memory_text[:-3]

        memory_text = memory_text.strip()

        # ==================================
        # Update Memory
        # ==================================
        try:

            new_memory = json.loads(memory_text)

            memory = update_memory(
                memory,
                new_memory,
            )

            save_memory(memory)

        except json.JSONDecodeError:

            print(
                "⚠️ Failed to update memory (Invalid JSON received)."
            )

        # ==================================
        # Save Chat History
        # ==================================
        save_history(history)

        # ==================================
        # Summarize Old Chats
        # ==================================
        if len(history) > SUMMARY_TRIGGER:

            old_messages = history[:-MAX_HISTORY]

            old_context = ""

            for msg in old_messages:
                old_context += (
                    f"{msg['role']}: {msg['content']}\n"
                )

            summary_prompt = build_summary_prompt(
                conversation_summary,
                old_context,
            )

            summary_response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=summary_prompt,
            )

            conversation_summary = summary_response.text

            save_summary(conversation_summary)

            history = history[-MAX_HISTORY:]

            save_history(history)

            print("📝 Conversation summarized!")

    except Exception as e:

        print(f"\n❌ Error: {e}\n")