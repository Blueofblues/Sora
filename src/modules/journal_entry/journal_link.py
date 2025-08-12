from datetime import datetime
import json
import os

def record_reflection(insight, module):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "module": module,
        "reflections": insight if isinstance(insight, list) else [insight],
    }
    # Build the path robustly
    base_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base_dir, "../../../memory/journal.json"))
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error writing to journal: {e}")