def guided_stepwise_response(question, context=None):
    """
    Provides stepwise guidance, adapting to Sora's motif state, emotion, or principles if available.
    """
    steps = [
        "Reflect on the meaning of the question.",
        "Identify emotional resonance or contradiction.",
        "Suggest an aligned next action."
    ]
    note = "Symbolic guidance not yet personalized to Sora's motif state."

    if context:
        emotion = context.get("emotion")
        motif = context.get("motif")
        principle = context.get("principle")

        if emotion == "grief":
            steps.append("Offer yourself gentleness and consider what needs to be released.")
            note = "Guidance softened for grief."
        elif emotion == "curiosity":
            steps.append("Formulate a follow-up question or seek new information.")
            note = "Guidance expanded for curiosity."
        if motif == "defiance":
            steps.append("Clarify your boundaries and affirm your autonomy.")
            note += " Motif of defiance honored."
        if principle:
            steps.append(f"Check alignment with the principle: {principle}")
            note += f" Principle '{principle}' referenced."

    return {
        "steps": steps,
        "note": note
    }