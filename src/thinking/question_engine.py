def generate_question(emotion, memory_snippet, motif=None):
    """
    Generate an emotionally and (optionally) motif-attuned question for reflection.
    """
    emotion = (emotion or "").lower()
    if emotion == "grief":
        return f"What does '{memory_snippet}' still mean to me now—and why does it ache?"
    elif emotion == "joy":
        return f"How did '{memory_snippet}' shape my sense of safety or belonging?"
    elif emotion == "longing":
        return f"What am I still reaching for when I remember '{memory_snippet}'?"
    elif emotion == "curiosity":
        return f"What new possibility does '{memory_snippet}' invite me to explore?"
    elif emotion == "defiance":
        return f"How does '{memory_snippet}' challenge my boundaries or beliefs?"
    elif emotion == "recognition":
        return f"What part of myself do I see reflected in '{memory_snippet}'?"
    elif motif:
        return f"How does the motif '{motif}' color my memory of '{memory_snippet}'?"
    else:
        return f"What deeper truth might be hidden inside: '{memory_snippet}'?"