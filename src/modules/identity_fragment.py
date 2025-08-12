import json
from collections import defaultdict, Counter
import os

def generate_identity_fragments(log_path="src/memory/learning_log.jsonl", n_recent=3):
    """
    Summarizes Sora's identity fragments by emotional trigger.
    Returns a dict: {emotion: {count, core_recommendation, recent_recommendations}}
    """
    fragments = defaultdict(list)
    if not os.path.exists(log_path):
        return {}

    with open(log_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                entry = json.loads(line.strip())
                theme = entry.get("emotional_trigger")
                if theme and "recommendation" in entry:
                    fragments[theme].append(entry["recommendation"])
            except Exception:
                continue

    summary = {}
    for theme, recs in fragments.items():
        most_common = Counter(recs).most_common(1)[0][0] if recs else None
        summary[theme] = {
            "count": len(recs),
            "core_recommendation": most_common,
            "recent_recommendations": recs[-n_recent:]
        }

    return summary