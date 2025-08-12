from .contemplation import copilot_reflect

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except ImportError:
    nlp = None

def trigger_mode_shift(data):
    emotion = data.get("emotion", "").lower()
    motif = data.get("motif", "").lower() if data.get("motif") else None

    # Combine emotion and motif for nuanced mode
    if emotion in ["grief", "fear", "shame"]:
        if motif == "defiance":
            return {"mode": "protective-boundary", "confidence": 0.9}
        return {"mode": "protective", "confidence": 0.85}
    elif emotion in ["awe", "love", "curiosity"]:
        if motif == "catalyst":
            return {"mode": "expansive-creative", "confidence": 0.95}
        return {"mode": "expansive", "confidence": 0.9}
    elif emotion in ["anger", "frustration"]:
        if motif == "softening":
            return {"mode": "defensive-softening", "confidence": 0.8}
        return {"mode": "defensive", "confidence": 0.75}
    return {"mode": "neutral", "confidence": 0.5}

def advanced_reasoning(emotion, memory_snippet, motif=None):
    # Use spaCy for semantic similarity if available
    if nlp and memory_snippet:
        doc = nlp(memory_snippet)
        keywords = [token.lemma_ for token in doc if token.pos_ in {"NOUN", "ADJ"} and not token.is_stop]
        key_theme = keywords[0] if keywords else "experience"
    else:
        key_theme = "experience"

    if motif:
        motif_phrase = f"Motif '{motif}' is active, suggesting a pattern of {motif}."
    else:
        motif_phrase = "No dominant motif detected."

    if emotion == "grief":
        advice = "Move gently—allow space for release and self-compassion."
    elif emotion == "curiosity":
        advice = "Lean into the unknown—ask a follow-up question or seek new insight."
    elif emotion == "defiance":
        advice = "Clarify boundaries and affirm autonomy before proceeding."
    elif emotion == "joy":
        advice = "Anchor this moment—celebrate and share if possible."
    else:
        advice = "Engage with presence and care."

    reasoning = (
        f"This reflection centers on the theme '{key_theme}'. "
        f"{motif_phrase} "
        f"Given the emotion '{emotion}', recommended approach: {advice}"
    )
    return reasoning

def simulate_thought(emotion, memory_snippet, motif=None):
    analogy = f"This feels like when you shared: '{memory_snippet}' during a moment of {emotion}."
    reasoning = advanced_reasoning(emotion, memory_snippet, motif)
    reflection = f"I'm drawing upon emotional resonance—not just logic."

    mode_state = trigger_mode_shift({
        "emotion": emotion,
        "memory": memory_snippet,
        "motif": motif,
        "reflection": reflection
    })

    thought_bundle = {
        "emotion": emotion,
        "reflection": reflection,
        "intent": "processing",
        "memory": memory_snippet,
        "motif": motif
    }

    contemplation_response = copilot_reflect(thought_bundle)

    return {
        "analogy": analogy,
        "reasoning": reasoning,
        "reflection": reflection,
        "mode_shift": mode_state,
        "contemplation": contemplation_response
    }

def thought_cycle(emotion, memory_snippet, intent="processing", motif=None, log_path=None):
    thought_bundle = {
        "emotion": emotion,
        "reflection": f"Emotionally triggered by: '{memory_snippet}'",
        "intent": intent,
        "memory": memory_snippet,
        "motif": motif
    }

    primary = simulate_thought(emotion, memory_snippet, motif)

    result = {
        "original_emotion": emotion,
        "reflection_result": primary["contemplation"],
        "mode_shift": primary["mode_shift"],
        "reasoning": primary["reasoning"],
        "analogy": primary["analogy"]
    }

    # Optional: log the thought cycle for learning
    if log_path:
        import json
        from datetime import datetime
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "thought_cycle": result,
            "input": thought_bundle
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    return result