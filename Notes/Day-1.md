# Day 1 – Building My First AI Chatbot (NainalaBot)

## 🎯 Goal

The objective of Day 1 was to understand how to communicate with a Large Language Model (LLM) using Python and the Gemini API by building a simple chatbot.

---

# What is an LLM?

**LLM (Large Language Model)** is an AI model trained on massive amounts of text data.

### Examples

- Gemini
- ChatGPT (GPT)
- Claude
- Llama

An LLM understands natural language and generates human-like responses.

> **Important:** We are **not building an LLM**. We are using one through an API.

---

# What is an API?

**API** stands for **Application Programming Interface**.

It allows one application to communicate with another.

### In our project:

```text
Python Program
       │
       ▼
Gemini API
       │
       ▼
Gemini LLM
       │
       ▼
Response
```

Instead of building an AI model ourselves, we send a request to Gemini and receive a response.

---

# Why do we need an API Key?

An API key is a unique secret provided by Google.

It is used to:

- Authenticate our application
- Track API usage
- Prevent unauthorized access

> Never hardcode API keys inside your source code.

---

# Why use a `.env` file?

A `.env` file stores sensitive information separately from the code.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

### Advantages

- Keeps secrets out of the source code
- Easy to change API keys
- Prevents accidentally uploading secrets to GitHub

---

# Why use `python-dotenv`?

The `python-dotenv` library loads environment variables from the `.env` file.

```python
from dotenv import load_dotenv

load_dotenv()
```

This makes the variables available using:

```python
os.getenv("GEMINI_API_KEY")
```

---

# Getting the API Key

We generated a free Gemini API key using **Google AI Studio**.

The API key was stored inside the `.env` file.

---

# Creating the Gemini Client

```python
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
```

This client allows our Python application to communicate with Gemini.

---

# Sending a Prompt

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=question,
)
```

### Explanation

- `model` → Specifies which Gemini model to use.
- `contents` → The user's input.
- `response` → Stores the AI's generated answer.

---

# Displaying the Response

```python
print(response.text)
```

The Gemini API returns a response object.

`response.text` contains the generated answer.

---

# Why use a `while` loop?

```python
while True:
```

The chatbot continues running until the user exits.

Without the loop, it would answer only one question and then terminate.

---

# Commands Added

We implemented several local commands.

| Command | Purpose                 |
| ------- | ----------------------- |
| `help`  | Show available commands |
| `hello` | Greeting                |
| `time`  | Display current time    |
| `clear` | Clear terminal          |
| `exit`  | Close chatbot           |

These commands are handled by Python itself without sending a request to Gemini.

---

# Why use `continue`?

Example:

```python
if command == "help":
    print("Available commands...")
    continue
```

`continue` skips the remaining code in the loop and starts the next iteration.

This prevents unnecessary API calls.

---

# Exception Handling

```python
try:
    ...
except Exception as e:
    print(e)
```

Exception handling prevents the chatbot from crashing when an error occurs.

---

# User Messages vs AI Requests

We introduced two counters.

## User Messages

Counts every message entered by the user.

## AI Requests

Counts only the prompts actually sent to Gemini.

---

# Current Project Flow

```text
User
   │
   ▼
Python Chatbot
   │
   ├── Local Commands
   │
   └── Gemini API
           │
           ▼
       Gemini LLM
           │
           ▼
       AI Response
```

---

# What We Built

By the end of Day 1, **NainalaBot** can:

- Accept user input
- Communicate with Gemini
- Display AI responses
- Execute local commands
- Handle errors gracefully
- Count user interactions
- Count AI requests

---

# Key Python Concepts Learned

- Virtual Environments (`venv`)
- Installing Packages with `pip`
- Environment Variables
- `.env` files
- `os.getenv()`
- `while` loops
- `if-elif-else`
- Exception Handling (`try-except`)
- Variables and counters

---

# Key AI Concepts Learned

- Large Language Models (LLMs)
- Gemini API
- API Keys
- Prompts
- Responses
- LLM Applications

---

# Interview Questions

1. What is an LLM?
2. What is an API?
3. Why do we need an API key?
4. Why should API keys be stored in a `.env` file?
5. What is `python-dotenv`?
6. What does `os.getenv()` do?
7. Why do we use a `while True` loop?
8. What is the purpose of `continue`?
9. What is exception handling?
10. What is the difference between user messages and AI requests?

---

# Summary

On Day 1, we built the first version of **NainalaBot**.

We learned how Python communicates with a Large Language Model using the Gemini API, implemented useful chatbot commands, handled errors gracefully, and followed best practices like virtual environments and environment variables.

---
