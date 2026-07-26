from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os
import json

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Create chat session (Gemini remembers conversation during this session)
chat = client.chats.create(
    model="gemini-2.5-flash-lite"
)

print("🤖 Welcome Tejasri!")
print("Type 'help' to see available commands.\n")

# Load previous chat history if it exists
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

# Counters
user_messages = 0
ai_requests = 0

while True:

    question = input("You: ").strip()

    if not question:
        print("⚠️ Please enter a message.\n")
        continue

    command = question.lower()

    # Exit
    if command == "exit":
        print("\n📊 Session Summary")
        print(f"Total Messages : {user_messages}")
        print(f"AI Requests    : {ai_requests}")
        print("👋 Goodbye!")
        break

    user_messages += 1

    # Help
    if command == "help":
        print("\n📋 Available Commands")
        print("----------------------")
        print("help     - Show available commands")
        print("hello    - Greet the bot")
        print("time     - Show current time")
        print("clear    - Clear the terminal")
        print("history  - Show stored conversation")
        print("exit     - Exit the chatbot\n")
        continue

    # Hello
    elif command == "hello":
        print("\n🤖 Hello Tejasri! 😊\n")
        continue

    # Time
    elif command == "time":
        current_time = datetime.now().strftime("%I:%M:%S %p")
        print(f"\n🕒 Current Time: {current_time}\n")
        continue

    # Clear terminal
    elif command == "clear":
        os.system("clear")  # Use "cls" for Windows
        continue

    # Show history
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

    # Store user message
    history.append({
        "role": "user",
        "content": question
    })
    context = ""
    for message in history:
        context += f"{message['role'].capitalize()}: {message['content']}"
    big_prompt = f"previous conversation : {context} + current question : {question}"
    try:
        response = chat.send_message(big_prompt)

        ai_requests += 1

        print(f"\n🤖 NainalaBot: {response.text}\n")

        # Store AI response
        history.append({
            "role": "model",
            "content": response.text
        })

        # Save updated history
        with open("chat_history.json", "w") as file:
            json.dump(history, file, indent=4)

    except Exception as e:
        print("\n❌ Unable to contact Gemini.")
        print(e)