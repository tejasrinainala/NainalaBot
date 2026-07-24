# 📅 Day 3 – Persistent Chat History with JSON

## 🎯 Goal

The goal of Day 3 was to make the chatbot remember previous conversations even after the program is closed by storing chat history in a JSON file.

---

## 📚 Concepts Learned

### 1. Temporary Memory vs Persistent Memory

Before today, the chatbot stored conversations only in RAM.

```python
history = []
```

When the program closed, all conversation history was lost.

Today I learned how to store conversation history permanently using a JSON file.

---

### 2. JSON Files

I learned that JSON is a lightweight format used to store structured data.

Example:

```json
[
    {
        "role": "user",
        "content": "Hi"
    },
    {
        "role": "model",
        "content": "Hello!"
    }
]
```

---

### 3. Reading JSON Files

I learned how to load previously saved conversations.

```python
with open("chat_history.json", "r") as file:
    history = json.load(file)
```

---

### 4. Writing JSON Files

After every conversation, the chatbot saves the updated history.

```python
with open("chat_history.json", "w") as file:
    json.dump(history, file, indent=4)
```

---

### 5. Checking Whether a File Exists

Instead of assuming the JSON file already exists, I learned how to check it.

```python
if os.path.exists("chat_history.json"):
```

If the file doesn't exist:

- Create an empty history list
- Create a new JSON file

---

## 🚀 Features Added

✅ Load previous conversations from JSON

✅ Automatically create `chat_history.json` if it doesn't exist

✅ Save every user message

✅ Save every AI response

✅ Auto-save after every conversation

✅ Added a `history` command to display stored conversations

---

## 📂 Project Flow

```
Start Program
      │
      ▼
Check if chat_history.json exists
      │
      ├── Yes → Load history
      │
      └── No → Create empty history
      │
      ▼
Start Chatbot
      │
      ▼
User sends message
      │
      ▼
Store user message
      │
      ▼
Gemini generates response
      │
      ▼
Store AI response
      │
      ▼
Save updated history to JSON
```

---

## ⚠️ Limitation

Although the conversation history is saved successfully, Gemini **does not remember previous chats after restarting the program**.

Reason:

Each time the program starts,

```python
chat = client.chats.create(...)
```

creates a brand-new chat session.

The chatbot stores conversations in `chat_history.json`, but those conversations are **not yet sent back to Gemini**.

So:

- ✅ My program remembers previous chats.
- ❌ Gemini starts with a fresh conversation after every restart.

---

## 💡 Key Takeaways

- Difference between RAM and persistent storage.
- Learned JSON file handling in Python.
- Learned `json.load()`.
- Learned `json.dump()`.
- Learned `os.path.exists()`.
- Understood why AI models don't automatically remember previous sessions.
- Built the foundation for persistent AI memory.
