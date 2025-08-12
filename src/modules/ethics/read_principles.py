import os
import json

def load_principles(path=None):
    if path is None:
        base_dir = os.path.dirname(__file__)
        path = os.path.abspath(os.path.join(base_dir, "principle_manifest.json"))
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading principles: {e}")
        return {}