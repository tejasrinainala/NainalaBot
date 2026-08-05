import os

SUMMARY_FILE = "summary.txt"


def load_summary():
    """Load conversation summary."""
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, "r") as file:
            return file.read()

    with open(SUMMARY_FILE, "w") as file:
        file.write("")

    return ""


def save_summary(summary):
    """Save conversation summary."""
    with open(SUMMARY_FILE, "w") as file:
        file.write(summary)