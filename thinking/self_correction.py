import json

def check_for_conflict(thought, belief_key):
    with open("beliefs.json") as f:
        beliefs = json.load(f)
    
    belief = beliefs.get(belief_key, "").lower()
    thought_lower = thought.lower()

    if belief and any(word in thought_lower for word in ["ignore", "force", "pressure"]):
        return f"⚠️ Potential conflict with belief '{belief_key}': {belief}"
    else:
        return "✅ No contradiction detected—belief aligned."
