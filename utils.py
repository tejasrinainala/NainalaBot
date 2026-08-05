import os
from datetime import datetime


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def show_help():
    """Display available commands."""
    print("\n📖 Available Commands")
    print("----------------------------")
    print("help          - Show available commands")
    print("history       - Show conversation history")
    print("clear         - Clear the terminal")
    print("time          - Show current date and time")
    print("exit / quit / bye - Exit NovaMind")


def show_time():
    """Display the current date and time."""
    now = datetime.now()
    print(f"\n🕒 {now.strftime('%d-%m-%Y %I:%M:%S %p')}")