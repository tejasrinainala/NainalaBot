# 📅 Day 6 - Long-Term Memory & Conversation Summarization

## ✅ What We Did

### 🧠 Implemented Long-Term Memory
- Created `memory.json` to store important user information.
- Stored user details such as name, city, education, preferences, and personal facts.
- Enabled NovaMind to remember users across multiple sessions.

---

### 📜 Added Memory Extraction
- Used Gemini to extract important information from user messages.
- Automatically updated `memory.json` with newly extracted facts.
- Ignored messages that did not contain useful long-term information.

---

### 📝 Implemented Conversation Summarization
- Added automatic summarization of older conversations.
- Stored summaries in `summary.txt`.
- Reduced the amount of conversation history sent to Gemini.

---

### 💬 Improved Prompt Context
Every request sent to Gemini now includes:
- Long-Term Memory (`memory.json`)
- Conversation Summary (`summary.txt`)
- Recent Chat History (`chat_history.json`)
- Current User Question

This helps NovaMind provide context-aware responses while keeping prompts efficient.

---

### 📂 Managed Chat History
- Preserved recent conversations in `chat_history.json`.
- Summarized older conversations once the history exceeded the defined limit.
- Prevented unlimited growth of chat history.

---

## 📚 Concepts Learned
- Long-Term Memory
- Memory Extraction
- Conversation Summarization
- Context Management
- Prompt Engineering
- JSON-based Data Storage

---

## 🎯 Day 6 Outcome

✅ Persistent Long-Term Memory

✅ Automatic Memory Extraction

✅ Conversation Summarization

✅ Efficient Context Management

NovaMind can now remember users across sessions while efficiently managing conversation context.
