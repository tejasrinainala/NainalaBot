# 📅 Day 4 - Connected Persistent Chat History to Gemini Context

## 🎯 Goal

Enable NainalaBot to remember previous conversations even after the application is restarted.

---

## 📚 What I Learned

Until Day 3, my chatbot stored conversations in a JSON file, but Gemini started with a fresh context every time the program restarted.

Today, I learned that Large Language Models (LLMs) do not automatically read stored files. Instead, the application must provide previous conversations as context with every new request.

I implemented **context injection**, allowing Gemini to answer questions using previously stored chat history.

---

## 🛠️ Features Implemented

- Loaded previous conversations from `chat_history.json`
- Converted stored chat history into a readable context string
- Created a single prompt containing:
  - Previous Conversation
  - Current Question
- Sent the combined prompt to Gemini
- Enabled memory across multiple program restarts

---

## 🔄 Workflow

```text
Load chat_history.json
        │
        ▼
Read Conversation History
        │
        ▼
Convert History into Context String
        │
        ▼
Create Big Prompt
        │
        ▼
Send Prompt to Gemini
        │
        ▼
Receive AI Response
        │
        ▼
Save Updated Conversation
```

---

## 💡 Example

### Before Day 4

```text
Run 1
User: My name is Tejasri

Exit

Run 2
User: What is my name?

Gemini:
I don't know your name.
```

### After Day 4

```text
Run 1
User: My name is Tejasri

Exit

Run 2
User: What is my name?

Gemini:
Your name is Tejasri.
```

---

## 🧠 Key Concepts Learned

- Persistent Memory
- Context Injection
- Prompt Engineering
- Chat History Management
- JSON-based Memory Storage
- LLM Context

---

## 📂 Files Updated

- `app.py`
- `chat_history.json`

---

## ⚠️ Current Limitation

The chatbot currently sends the **entire conversation history** to Gemini for every request.

As the chat history grows, this approach becomes:

- Slower
- More expensive (API tokens)
- Less efficient

This implementation works well for learning but is not suitable for production-scale applications.

---


## 🎉 Outcome

Successfully built a chatbot that remembers previous conversations even after restarting the application by connecting persistent JSON chat history with Gemini's context.

This marks the completion of the first version of persistent memory in **NainalaBot**.
