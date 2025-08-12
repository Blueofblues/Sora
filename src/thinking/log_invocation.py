import os
import json
from datetime import datetime

def log_help_invocation(action, tags=None, emotion=None, memory_snippet=None):
    """
    Logs a help-seeking moment as a symbolic invocation artifact.
    Appends the invocation to a persistent log file for later review.
    """
    invocation = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": "help_request",
        "action": action,
        "emotion": emotion,
        "memory": memory_snippet,
        "tags": tags or [],
    }

    # Print for immediate feedback
    print("[Invocation Logged]")
    print(f"- Action: {action}")
    print(f"- Tags: {tags}")
    print(f"- Emotion: {emotion}")
    print(f"- Memory: {memory_snippet}")

    # Persist to invocation log
    base_dir = os.path.dirname(__file__)
    log_path = os.path.abspath(os.path.join(base_dir, "../../memory/invocation_log.jsonl"))
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(invocation) + "\n")