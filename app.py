from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("🤖 Welcome Tejasri!")
print("Type 'help' to see available commands.\n")

# Counters
user_messages = 0
ai_requests = 0

while True:
    # Get user input
    question = input("You: ").strip()

    # Ignore empty input
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

    # Count every user message except exit
    user_messages += 1

    # Help
    if command == "help":
        print("\n📋 Available Commands")
        print("----------------------")
        print("help  - Show available commands")
        print("hello - Greet the bot")
        print("time  - Show current time")
        print("clear - Clear the terminal")
        print("exit  - Exit the chatbot\n")
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
        os.system("clear")      # macOS/Linux
        # os.system("cls")       # Windows
        continue

    # Ask Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=question
        )

        ai_requests += 1

        print(f"\n🤖 NainalaBot: {response.text}\n")

    except Exception as e:
        print("\n❌ Unable to contact Gemini.")
        print(e)