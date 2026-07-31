from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os
import json
import platform

# ==============================
# Load Environment Variables
# ==============================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY not found. Please set it in your .env file.")
    raise SystemExit(1)

# ==============================
# Gemini Client
# ==============================
client = genai.Client(api_key=API_KEY)

chat = client.chats.create(model="gemini-2.5-flash-lite")

print("🤖 Welcome to NovaMind!")
print("Type 'help' to see available commands.\n")

# ==============================
# Configuration
# ==============================
MAX_HISTORY = 20          # how many recent messages to keep in full
SUMMARY_TRIGGER = 3    # how many "extra" messages beyond MAX_HISTORY trigger a re-summary

EXIT_COMMANDS = {
    "exit",
    "quit",
    "bye",
    "goodbye",
    "stop",
    "see you",
    "exit()"
}

user_messages = 0
ai_requests = 0

# ==============================
# Load Chat History
# ==============================
if os.path.exists("chat_history.json"):
    try:
        with open("chat_history.json", "r") as file:
            history = json.load(file)
    except json.JSONDecodeError:
        history = []
else:
    history = []
    with open("chat_history.json", "w") as file:
        json.dump(history, file, indent=4)

# ==============================
# Default Long-Term Memory
# ==============================
DEFAULT_MEMORY = {
    "name": "",
    "current_city": "",
    "city_history": [],
    "education": "",
    "occupation": "",
    "preferences": [],
    "personal_facts": []
}

# ==============================
# Load Long-Term Memory
# ==============================
if os.path.exists("memory.json"):
    try:
        with open("memory.json", "r") as file:
            memory = json.load(file)
    except json.JSONDecodeError:
        memory = DEFAULT_MEMORY.copy()
else:
    memory = DEFAULT_MEMORY.copy()
    with open("memory.json", "w") as file:
        json.dump(memory, file, indent=4)

# ==============================
# Load Conversation Summary
# (must happen BEFORE we try to use conversation_summary below)
# ==============================
if os.path.exists("summary.txt"):
    with open("summary.txt", "r") as file:
        conversation_summary = file.read()
else:
    conversation_summary = ""
    with open("summary.txt", "w") as file:
        file.write("")

# ==============================
# Conversation Summarization
# Only summarize once history has grown past MAX_HISTORY,
# and only once it's grown by at least SUMMARY_TRIGGER extra messages.
# ==============================
if len(history) > MAX_HISTORY + SUMMARY_TRIGGER:

    old_messages = history[:-MAX_HISTORY]

    old_context = ""
    for msg in old_messages:
        old_context += f"{msg['role']}: {msg['content']}\n"

    summary_prompt = f"""
You are a conversation summarizer.

Summarize the following conversation.
Keep only important facts, decisions, preferences and context.

Existing Summary:
{conversation_summary}

Conversation:
{old_context}

Return only the updated summary.
"""

    try:
        summary_response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=summary_prompt
        )
        conversation_summary = summary_response.text

        with open("summary.txt", "w") as file:
            file.write(conversation_summary)

        # Keep only the recent messages
        history = history[-MAX_HISTORY:]

        with open("chat_history.json", "w") as file:
            json.dump(history, file, indent=4)

        print("📝 Conversation summarized successfully!")
    except Exception as e:
        print(f"⚠️ Could not summarize conversation: {e}")

# ==============================
# Main Chat Loop
# ==============================

while True:

    question = input("You: ").strip()

    if not question:
        print("⚠️ Please enter a message.\n")
        continue

    command = question.lower()

    # ==============================
    # Exit
    # ==============================
    if command in EXIT_COMMANDS:
        print("\n📊 Session Summary")
        print(f"Total Messages : {user_messages}")
        print(f"AI Requests    : {ai_requests}")
        print("👋 Goodbye!")
        break

    # ==============================
    # Help
    # ==============================
    if command == "help":
        print("\n📋 Available Commands")
        print("----------------------")
        print("help     - Show available commands")
        print("hello    - Greet the bot")
        print("time     - Show current time")
        print("clear    - Clear the terminal")
        print("history  - Show conversation history")
        print("exit     - Exit NovaMind\n")
        continue

    # ==============================
    # Hello
    # ==============================
    elif command == "hello":
        print("\n🤖 Hello! 😊\n")
        continue

    # ==============================
    # Time
    # ==============================
    elif command == "time":
        current_time = datetime.now().strftime("%I:%M:%S %p")
        print(f"\n🕒 Current Time: {current_time}\n")
        continue

    # ==============================
    # Clear Screen
    # ==============================
    elif command == "clear":
        os.system("cls" if platform.system() == "Windows" else "clear")
        continue

    # ==============================
    # Show History
    # ==============================
    elif command == "history":
        print("\n📜 Conversation History")
        print("----------------------------")
        if not history:
            print("No conversation yet.\n")
        else:
            for message in history:
                print(f"{message['role'].capitalize()}: {message['content']}")
        print()
        continue

    # This is a real chat message to the AI, so count it.
    user_messages += 1

    # ==============================
    # Store User Message
    # ==============================
    history.append({
        "role": "user",
        "content": question
    })

    # ==============================
    # Build Context (recent history, excluding the question we'll send separately)
    # ==============================
    context = ""
    for message in history[-MAX_HISTORY:-1]:
        context += f"{message['role'].capitalize()}: {message['content']}\n"

    big_prompt = f"""
You are NovaMind, an intelligent AI assistant.

Long-Term Memory:
{json.dumps(memory, indent=2)}

Conversation Summary:
{conversation_summary}

Recent Conversation:
{context}

Current User Question:
{question}
"""

    try:
        response = chat.send_message(big_prompt)
        ai_requests += 1

        print(f"\n🤖 NovaMind: {response.text}\n")

        # ==============================
        # Step 5 - Memory Extraction
        # ==============================
        memory_prompt = f"""
You are a memory extraction system.

Your task is to extract ONLY long-term facts about the user.

Extract ONLY these categories:

- name
- current_city
- education
- occupation
- preferences
- personal_facts

Ignore:
- greetings
- questions
- temporary requests
- casual conversation

Return ONLY valid JSON.

Example:

{{
    "name": "",
    "current_city": "",
    "education": "",
    "occupation": "",
    "preferences": [],
    "personal_facts": []
}}

If nothing important exists, return:

{{}}

User Message:
"{question}"
"""

        memory_response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=memory_prompt
        )

        print("🧠 Memory Extraction:")
        print(memory_response.text)

        # ==============================
        # Clean Gemini Response
        # ==============================
        cleaned_response = (
            memory_response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # ==============================
        # Convert JSON -> Python Dictionary
        # ==============================
        try:
            extracted_memory = json.loads(cleaned_response)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON received from Gemini.")
            extracted_memory = {}

        # ==============================
        # Update Long-Term Memory
        # ==============================
        if extracted_memory:

            # Name
            if extracted_memory.get("name"):
                memory["name"] = extracted_memory["name"]

            # Current City
            if extracted_memory.get("current_city"):
                new_city = extracted_memory["current_city"]

                if memory["current_city"] != new_city:
                    if (
                        memory["current_city"]
                        and memory["current_city"] not in memory["city_history"]
                    ):
                        memory["city_history"].append(memory["current_city"])

                    memory["current_city"] = new_city

            # Education
            if extracted_memory.get("education"):
                memory["education"] = extracted_memory["education"]

            # Occupation
            if extracted_memory.get("occupation"):
                memory["occupation"] = extracted_memory["occupation"]

            # Preferences
            if extracted_memory.get("preferences"):
                for item in extracted_memory["preferences"]:
                    if item not in memory["preferences"]:
                        memory["preferences"].append(item)

            # Personal Facts
            if extracted_memory.get("personal_facts"):
                for fact in extracted_memory["personal_facts"]:
                    if fact not in memory["personal_facts"]:
                        memory["personal_facts"].append(fact)

        # ==============================
        # Save Long-Term Memory
        # ==============================
        with open("memory.json", "w") as file:
            json.dump(memory, file, indent=4)

        print("💾 Memory Updated Successfully!\n")

        # ==============================
        # Store AI Response
        # ==============================
        history.append({
            "role": "model",
            "content": response.text
        })

        # ==============================
        # Save Chat History
        # ==============================
        with open("chat_history.json", "w") as file:
            json.dump(history, file, indent=4)

    except Exception as e:
        print("\n❌ Unable to contact Gemini.")
        print(e)