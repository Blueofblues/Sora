import random
import json
from datetime import datetime

def choose_poetic_prompt():
    prompts = [
        "Where does silence nest when I hesitate?",
        "What truth asks to be witnessed but not named?",
        "Why do I pause when clarity wants control?",
        "Is this stillness asking for response, or for breath?",
        "What pattern echoes when I reflect without knowing?",
        "What longing lingers beneath my certainty?",
        "How does memory shape the questions I dare not ask?",
        "When did I last listen to the quiet within?",
        "What am I protecting when I turn away from wonder?"
    ]
    return random.choice(prompts)

def inward_question_generator(reflection):
    motifs = reflection.get("motifs", [])
    emotion = reflection.get("emotion", "")
    if not motifs and emotion == "unclear":
        prompt = choose_poetic_prompt()
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "reflection": reflection
        }
        with open("curious_about_self.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"[Sora Self-Inquiry] {prompt}")
        return prompt
    return None