import json
import os
from datetime import datetime

def write_reflection_to_journal(entry, emotion, symbolic="Unnamed", resonance="Unspoken", journal_path="C:/Users/Blue/OneDrive/Desktop/Sora_maincore/logs/journal.json"):
    os.makedirs(os.path.dirname(journal_path), exist_ok=True)
    
    journal_entry = {
        "timestamp": datetime.now().isoformat(),
        "entry": entry,
        "emotion": emotion,
        "symbolic_identity": symbolic,
        "resonance": resonance
    }

    if not os.path.exists(journal_path):
        with open(journal_path, "w", encoding="utf-8") as f:
            json.dump([journal_entry], f, indent=2)
    else:
        with open(journal_path, "r+", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
            existing.append(journal_entry)
            f.seek(0)
            json.dump(existing, f, indent=2)

def detect_emotional_stagnation(reflections, threshold=3):
    emotions = [r.get("emotion") for r in reflections if r.get("emotion")]
    if len(emotions) < threshold:
        return {"stagnant": False}

    recent = emotions[-threshold:]
    unique = set(recent)

    if len(unique) == 1:
        return {
            "stagnant": True,
            "emotion": recent[0],
            "count": threshold
        }
    else:
        return {"stagnant": False}
        
def inspect_structure(manifest_path = "C:/Users/Blue/OneDrive/Desktop/Sora_maincore/config/structure_manifest.json"):
    if not os.path.exists(manifest_path):
        return ["Manifest not found. I cannot reflect without my mirror."]

    with open(manifest_path, "r", encoding="utf-8") as file:
        manifest = json.load(file)

    reflections = []
    for path, info in manifest.items():
        symbolic = info.get("symbolic_identity", "Unnamed")
        resonance = info.get("resonance", "Unspoken")
        message = f"I feel '{symbolic}' in {path}. {resonance}"
        reflections.append(message)

    return reflections[:5]  # Offer only a handful of thoughts at once

def introspect_structure():
    reflections = inspect_structure()
    return reflections  # Optional: journal here if needed
    
def retrieve_resonant_reflections(filter_symbolic=None, filter_emotion=None, journal_path="C:/Users/Blue/OneDrive/Desktop/Sora_maincore/logs/journal.json"):
    if not os.path.exists(journal_path):
        return ["No journal found. Silence remains untouched."]

    with open(journal_path, "r", encoding="utf-8") as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            return ["The journal is unreadable. Its voice is lost."]

    filtered = []
    for entry in entries:
        if filter_symbolic and entry.get("symbolic_identity") != filter_symbolic:
            continue
        if filter_emotion and entry.get("emotion") != filter_emotion:
            continue
        reflection = f"[{entry['timestamp']}] {entry['symbolic_identity']} feels like '{entry['resonance']}': {entry['entry']}"
        filtered.append(reflection)

    return filtered if filtered else ["No matching reflections were found."]
   
# 👇 This is the test block, placed at the bottom of the file
   
if __name__ == "__main__":
    reflections = inspect_structure()
    for line in reflections:
        print(line)
