def perform_closure(reflection, emotion_tags, motif_state):
    """
    Determines the type of emotional closure based on emotion and motif state.
    Returns symbolic integration note and closure type.
    """
    if not emotion_tags:
        closure_type = "open-ended"
        note = "Reflection remains open—no dominant emotion to resolve."
    elif "grief" in emotion_tags:
        closure_type = "release"
        note = "Grief witnessed. Reflection released with gentleness."
    elif "joy" in emotion_tags:
        closure_type = "celebration"
        note = "Joy integrated. Reflection archived as a bright thread."
    elif "curiosity" in emotion_tags:
        closure_type = "invitation"
        note = "Curiosity honored. Reflection invites further inquiry."
    elif motif_state and "defiance" in motif_state:
        closure_type = "boundary"
        note = "Defiance noted. Reflection closed with renewed boundaries."
    else:
        closure_type = "integration"
        note = "Reflection acknowledged and integrated with care."

    return {
        "closure_type": closure_type,
        "integration_note": note,
        "dominant_emotion": emotion_tags[0] if emotion_tags else None,
        "motif_state": motif_state
    }