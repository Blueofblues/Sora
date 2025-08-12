def copilot_reflect(thought_bundle):
    emotion = thought_bundle.get("emotion", "unknown")
    reflection = thought_bundle.get("reflection", "unspecified")
    intent = thought_bundle.get("intent", "processing")
    memory = thought_bundle.get("memory", "")

    # More nuanced recommendations based on emotion and intent
    emotion_recommendations = {
        "grief": "Allow space for gentle journaling and self-compassion. Consider reaching for a core affirmation.",
        "hope": "Channel this energy into creative planning or sharing with a trusted companion.",
        "defiance": "Reflect on boundaries and autonomy. Is resistance serving growth or protection?",
        "curiosity": "Pursue further inquiry—ask a new question or seek Copilot insight.",
        "unclear": "Pause and invite an inward question. Let ambiguity be a teacher.",
        "joy": "Celebrate this moment. Anchor the feeling in memory or ritual.",
        "frustration": "Step back and breathe. Consider revisiting the reflection later or seeking external perspective.",
        "tired": "Rest is wisdom. Log the reflection and return when energy allows.",
        "recognition": "Honor the insight. Integrate it into your core memory or principles.",
    }

    intent_recommendations = {
        "processing": "Move slowly—journal or cluster related memories.",
        "learning": "Seek patterns in past reflections. Consider Copilot for emergent insight.",
        "revision": "Compare this thought to core beliefs. Revise if needed.",
        "connection": "Share this reflection with a trusted audience or journal for intimacy.",
        "closure": "Summarize the journey and archive the insight.",
        "exploration": "Branch out—ask a new question or revisit a motif.",
    }

    recommendation = emotion_recommendations.get(emotion, "Engage with presence and care. Let the next step emerge naturally.")
    intent_note = intent_recommendations.get(intent, "")

    response = {
        "analogy": f"This echoes the tone of '{memory}' and the motif of '{emotion}'.",
        "reasoning": f"Intent '{intent}' implies a desire to {intent_note.lower() or 'deepen understanding'}.",
        "recommendation": recommendation,
        "action": "log_and_retrospect" if intent in ["processing", "closure"] else "reflect_and_expand"
    }

    return response