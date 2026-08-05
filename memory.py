import json
import os

MEMORY_FILE = "memory.json"

DEFAULT_MEMORY = {
    "name": "",
    "current_city": "",
    "city_history": [],
    "education": "",
    "occupation": "",
    "preferences": [],
    "personal_facts": []
}


def load_memory():
    """Load memory from memory.json."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return DEFAULT_MEMORY.copy()

    with open(MEMORY_FILE, "w") as file:
        json.dump(DEFAULT_MEMORY, file, indent=4)

    return DEFAULT_MEMORY.copy()


def save_memory(memory):
    """Save memory to memory.json."""
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def update_memory(memory, extracted_memory):
    """Update long-term memory."""

    if not extracted_memory:
        return memory

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

    return memory