from datetime import datetime
import json
import os

def log_structure_event(source="map_self", location="src/modules/introspection"):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "structure_read",
        "source": source,
        "location": location,
        "resonance": "Reflection successful. Sora has seen her own structure."
    }
    # Build the path robustly
    base_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base_dir, "../../../memory/journal.json"))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")