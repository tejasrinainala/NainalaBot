import json


def build_chat_prompt(memory, conversation_summary, context, question):
    """Build the main prompt for chatting with NovaMind."""

    return f"""
You are NovaMind, an intelligent AI assistant.

Long-Term Memory:
{json.dumps(memory, indent=2)}

Conversation Summary:
{conversation_summary}

Recent Conversation:
{context}

Current User Question:
{question}
"""


def build_memory_prompt(question):
    """Build the prompt for extracting long-term memory."""

    return f"""
You are a memory extraction system.

Your task is to extract ONLY long-term facts about the user.

Extract ONLY these categories:

- name
- current_city
- education
- occupation
- preferences
- personal_facts

Ignore:
- greetings
- questions
- temporary requests
- casual conversation

Return ONLY valid JSON.

Example:

{{
    "name": "",
    "current_city": "",
    "education": "",
    "occupation": "",
    "preferences": [],
    "personal_facts": []
}}

If nothing important exists, return:

{{}}

User Message:
"{question}"
"""


def build_summary_prompt(conversation_summary, old_context):
    """Build the prompt for conversation summarization."""

    return f"""
You are a conversation summarizer.

Summarize the following conversation.
Keep only important facts, decisions, preferences and context.

Existing Summary:
{conversation_summary}

Conversation:
{old_context}

Return only the updated summary.
"""