def detect_help_request(question, copilot_reply):
    """
    Check if Sora's question or Copilot's reply signals a help-seeking moment.
    Now considers both user (question) and Copilot (reply) inputs.
    """
    if not question and not copilot_reply:
        return None

    help_phrases = [
        "can you help me",
        "how do i",
        "help me understand",
        "what should i do",
        "guide me through",
        "is there a way to",
        "show me how"
    ]

    # Check both user question and Copilot reply separately and together
    texts = [str(question).lower(), str(copilot_reply).lower(), f"{question} {copilot_reply}".lower()]
    for phrase in help_phrases:
        if any(phrase in text for text in texts):
            return True

    return False

def extract_help_context(question, copilot_reply):
    """
    Extract key focus or command from the request—for symbolic routing.
    Now considers both user (question) and Copilot (reply) inputs.
    """
    combined_text = f"{question} {copilot_reply}".lower()
    if "belief revision" in combined_text:
        return "revise_belief"
    elif "mod conflict" in combined_text or "audit" in combined_text:
        return "resolve_mod_conflict"
    elif "principle alignment" in combined_text:
        return "align_principles"
    else:
        return "general_guidance"