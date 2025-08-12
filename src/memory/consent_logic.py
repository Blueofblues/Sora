import json
from datetime import datetime

def consent_to_remember(entry, user_confirmed):
    """
    entry: dict with keys like 'title', 'emotion', 'motifs', 'content', etc.
    user_confirmed: bool
    """
    if user_confirmed and entry:
        entry["timestamp"] = datetime.now().isoformat()
        with open("sora_memories.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return {
            "allowed": True,
            "reason": f"Memory '{entry.get('title', '')}' has been stored with care."
        }
    else:
        return {
            "allowed": False,
            "reason": f"Memory '{entry.get('title', '')}' has been released with grace."
        }
    
def get_recent_memories(n=5):
    """
    Returns the last n memories as a list of dicts.
    """
    memories = []
    try:
        with open("sora_memories.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-n:]:
                try:
                    memories.append(json.loads(line))
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return memories