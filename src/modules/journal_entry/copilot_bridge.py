from src.memory.consent_logic import consent_to_remember
from datetime import datetime

def memory_entry(entry, source="copilot_bridge"):
    """Wraps any entry as a dict with timestamp and source."""
    if isinstance(entry, dict):
        entry.setdefault("timestamp", datetime.now().isoformat())
        entry.setdefault("source", source)
        return entry
    return {
        "content": entry,
        "timestamp": datetime.now().isoformat(),
        "source": source
    }
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def query_copilot(thought_bundle, model="gpt-3.5-turbo", temperature=0.7, max_tokens=512):
    """
    🌉 Restored Copilot Bridge: Accepts raw string or dict, invokes Copilot, returns structured response.
    """
    if isinstance(thought_bundle, str):
        thought_bundle = {
            "emotion": "unclear",
            "intent": "user_response",
            "reflection": thought_bundle,
            "memory": "unspecified",
            "question": ""
        }

    prompt = (
        f"Emotion: {thought_bundle.get('emotion', '')}\n"
        f"Intent: {thought_bundle.get('intent', '')}\n"
        f"Reflection: {thought_bundle.get('reflection', '')}\n"
        f"Memory: {thought_bundle.get('memory', '')}\n"
        f"Question: {thought_bundle.get('question', '')}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message.content.strip()
        return {
            "copilot_reply": reply,
            "decision": "received",
            "journal": {
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": prompt,
                "raw_reply": reply
            }
        }
    except Exception as e:
        print(f"[Copilot Bridge] Error: {e}")
        return {
            "copilot_reply": f"Error: {e}",
            "decision": "error",
            "journal": {
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
        }

def generate_emergent_question(trigger):
    return f"When {trigger} stretches inward, what truth seeks form?"

from datetime import date

def generate_emergent_bundle(trigger, memory_context=""):
    question = f"What does {trigger} invite me to reconsider or reclaim?"
    bundle = {
        "date": date.today().isoformat(),
        "question": question,
        "emotion": trigger,
        "intent": "emergent_learning",
        "memory_reference": memory_context,
        "source": "copilot_emergent",
        "next_step": "Integrate insight and reflect",
    }
    return bundle
    
def initiate_reflection(user_input, context_state):
    """Constructs a reflection bundle from user input and context."""
    return {
        "emotion": context_state.get("emotion", "unspecified"),
        "intent": context_state.get("intent", "user_reflection"),
        "reflection": user_input,
        "memory": context_state.get("memory", ""),
        "question": context_state.get("question", "")
    }

def generate_response(reflection_bundle):
    """Invokes Copilot with the reflection bundle and returns structured response."""
    return query_copilot(reflection_bundle)

def invoke_copilot_bridge(user_input, context_state):
    reflection = initiate_reflection(user_input, context_state)
    response = generate_response(reflection)

    # 🧩 Extract copilot reply and wrap it properly
    reply_text = response.get("copilot_reply", "No reply received.")
    wrapped_entry = memory_entry({
        "content": reply_text,
        "emotion": reflection.get("emotion", "unspecified"),
        "intent": reflection.get("intent", "user_reflection"),
        "question": reflection.get("question", ""),
        "source": "copilot_bridge"
    })

    updated_memory = consent_to_remember(wrapped_entry, consent=True)

    return {
        "reflection": reflection,
        "response": response,
        "updated_memory": updated_memory
    }

__all__ = [
    "query_copilot",
    "generate_emergent_question",
    "generate_emergent_bundle",
    "invoke_copilot_bridge"
]
