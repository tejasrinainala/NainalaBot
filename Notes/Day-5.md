# 🚀 Day 5 - Conversation History Optimization

## 📌 Overview

Day 5 focuses on optimizing conversation memory and improving the overall user experience of NovaMind.

Instead of sending the entire chat history to Gemini, the chatbot now sends only the most recent conversations, reducing unnecessary token usage and improving performance.

---

## ✨ Features Added

### 🔹 Conversation History Trimming

- Introduced a configurable `MAX_HISTORY` variable.
- Only the latest 20 messages are included in the prompt sent to Gemini.

```python
MAX_HISTORY = 20
```

This helps:
- ⚡ Improve response speed
- 💰 Reduce token usage
- 📉 Decrease prompt size
- 📈 Improve scalability

---

### 🔹 Optimized Prompt Construction

The chatbot now builds prompts using only the recent conversation.

Example:

```
Previous Conversation:
User: Hello
Model: Hi!
User: How are you?

Current Question:
What's my name?
```

---

### 🔹 Multiple Exit Commands

Users can now end the chatbot using different commands instead of only `exit`.

Supported commands:

- exit
- quit
- bye
- goodbye
- stop
- see you
- exit()

This improves usability and prevents unnecessary API requests.

---

## 📚 Concepts Learned

- Python List Slicing
- Context Window
- Prompt Engineering
- Token Optimization
- Conversation Trimming
- User Experience (UX)
- Command Handling

---

## 🛠 Tech Stack

- Python
- Google Gemini API
- JSON
- python-dotenv

---

## 📈 Improvements

- Faster prompt generation
- Better memory management
- Reduced API token usage
- More natural chatbot interaction
- Cleaner command handling
