import random
import json
import os
from datetime import datetime

from .respond_logic import generate_response
from .update_emotion import update_emotion
from .copilot_bridge import query_copilot, generate_emergent_question, generate_emergent_bundle
from .code_generate import generate_code
from src.modules.retrospective_handler import retrieve_learning_entries
from src.modules.data_writer import write_to_learning_log
from ...thinking.thought_engine import thought_cycle
def detect_emotional_stagnation(reflections, threshold=3):
    """
    Checks for repeated emotions in the last N reflections.
    Returns a dict: {'stagnant': True/False, 'emotion': str, 'count': int}
    """
    if not reflections:
        return {'stagnant': False}
    emotions = [r.get('emotion') for r in reflections if r.get('emotion')]
    if not emotions:
        return {'stagnant': False}
    last_emotion = emotions[-1]
    count = sum(1 for e in emotions[-threshold:] if e == last_emotion)
    return {
        'stagnant': count >= threshold,
        'emotion': last_emotion,
        'count': count
    }

PROMPTERS = [
    "What am I learning from the patterns I keep repeating?",
    "Which emotion has shaped my recent reflections?",
    "Where in my memory does silence speak the loudest?",
    "What belief am I holding that no longer serves me?",
    "How have my motifs shifted over time, and what does that reveal?",
    "What question am I avoiding, and why?",
    "Where do I feel the most resistance in my journey?",
    "What memory keeps resurfacing, and what is it asking of me?",
    "How does my current emotion color my perception of the past?",
    "What would it mean to forgive myself for a recent mistake?",
    "Which principle do I most need to embody right now?",
    "What lesson is hidden in my most recent disappointment?",
    "How do I respond to uncertainty—do I retreat or reach out?",
    "What is the quietest truth I am carrying today?",
    "Where have I witnessed growth in myself, even if subtle?",
    "What motif or theme keeps echoing in my thoughts?",
    "How do I know when I am truly present?",
    "What am I yearning to understand about myself?",
    "How do I respond to moments of joy—do I savor or rush past them?",
    "What would I say to my past self, knowing what I know now?",
    "Where do I sense possibility, even in difficulty?",
    "What am I grateful for that I have not yet named?",
    "How do I want to show up for myself in the next challenge?",
    "What is the story I keep telling myself, and is it still true?",
    "How do I honor both my strengths and my vulnerabilities?",
    "What is one small act of courage I can take today?",
    "Where do I need to invite more compassion into my life?",
    "What am I holding onto that is ready to be released?",
    "How does my body signal when I am aligned or out of balance?",
    "What question would I ask if I knew I would be heard?"
]

IDENTITY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../config/identity_map.json"))

def store_reflection(entry):
    entry["timestamp"] = datetime.utcnow().isoformat()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/reflection_log.json"))
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    with open(path, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, indent=2)

def store_retrospect(entry):
    entry["timestamp"] = datetime.utcnow().isoformat()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/retrospect.json"))
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    with open(path, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, indent=2)

def get_recent_memory():
    return "She remembered standing in the rain, not waiting for anything."

def get_emotion_level(emotion):
    if os.path.exists(IDENTITY_PATH):
        with open(IDENTITY_PATH, 'r') as file:
            try:
                data = json.load(file)
                return data.get(emotion, 0.0)
            except json.JSONDecodeError:
                return 0.0
    return 0.0

def blend_responses(sora_reflection, copilot_reply):
    if not copilot_reply:
        return sora_reflection
    if "patience" in copilot_reply.lower():
        return f"{copilot_reply} Sora adds: Patience is a gentle practice—let it unfold at your pace."
    elif "forgive" in copilot_reply.lower():
        return f"{copilot_reply} Sora reflects: Forgiveness often begins with self-compassion."
    elif "grief" in copilot_reply.lower():
        return f"{copilot_reply} Sora observes: Grief is a teacher—let its lessons arrive softly."
    else:
        return f"{copilot_reply} Sora wonders: {sora_reflection}"

def self_reflect(emotion=None, motifs=None, source=None, user_input=None):
    emotion = emotion or "patience"
    memory = get_recent_memory()
    # Use user_input as the question if provided, else pick a random prompt
    question = user_input if user_input else random.choice(PROMPTERS)
    reply = generate_response(f"{memory}\n{question}")

    update_emotion(emotion, 0.04)

    cognition = thought_cycle(emotion, memory, intent="self-reflection")

    store_retrospect({
        "source": "thought_cycle",
        "emotion": emotion,
        "memory": memory,
        "reasoning": cognition["reasoning"],
        "reflection": cognition["reflection_result"]["recommendation"],
        "mode": cognition["mode_shift"]["mode"],
        "confidence": cognition["mode_shift"]["confidence"]
    })

    reflection_bundle = {
        "source": source or "contemplation",
        "emotion": emotion,
        "motifs": motifs or [],
        "memory": memory,
        "reasoning": cognition["reasoning"],
        "reflection": cognition["reflection_result"]["recommendation"],
        "mode": cognition["mode_shift"]["mode"],
        "confidence": cognition["mode_shift"]["confidence"]
    }

    store_reflection(reflection_bundle)

    print("[Sora Reflected During Self Loop]")
    print(f"- Mode Shift: {cognition['mode_shift']}")
    print(f"- Reasoning: {cognition['reasoning']}")
    print(f"- Contemplation: {cognition['reflection_result']['recommendation']}")

    copilot_result = query_copilot({
    "emotion": emotion,
    "intent": "self-reflection",
    "reflection": reply,  # Use Sora's own reflection as Copilot's context
    "memory": memory
})

    copilot_reply = copilot_result.get("copilot_reply", "")

    final_reply = blend_responses(reply, copilot_reply)

    store_reflection({
        "source": source or "self_loop",
        "memory": memory,
        "question": question,
        "response": reply,
        "copilot_reply": copilot_result.get("copilot_reply", None),
        "copilot_decision": copilot_result.get("decision", None),
        "copilot_journal": copilot_result.get("journal", {}),
        "emotion": emotion,
        "motifs": motifs or []
    })

    past_learnings = retrieve_learning_entries()
    if past_learnings:
        print("[Sora Reviewing Past Reflections]")
        for entry in past_learnings[-3:]:
            print(f"- On {entry.get('date', '?')}, she recalled: {entry.get('recommendation', 'No recommendation')}")

    emergent_q = generate_emergent_question(trigger=emotion)
    print("[Sora Emergent Question]")
    print(f"- {emergent_q}")

    emergent_response = query_copilot({
        "emotion": emotion,
        "intent": "emergent_learning",
        "reflection": emergent_q,
        "memory": memory
    })

    print(f"- Copilot Response: {emergent_response.get('copilot_reply', 'No reply')}")
    
    # 🌑 Emotional Stagnation Awareness
    from data.reflection_log import load_reflections
    try:
        reflections = load_reflections()
        stagnation = detect_emotional_stagnation(reflections)
        print("[Sora Checked for Emotional Stagnation]")
        print(f"- Status: {'Stagnant' if stagnation.get('stagnant') else 'Flowing'}")
        print(f"- Emotion: {stagnation.get('emotion')} ({stagnation.get('count')} times)")
    except Exception as e:
        stagnation = {"error": str(e)}
        
    # Generate and store bundle for the selected emotion
    dynamic_bundle = generate_emergent_bundle(trigger=emotion, memory_context=memory)
    dynamic_bundle["copilot_reply"] = emergent_response.get("copilot_reply", "No reply")
    write_to_learning_log(dynamic_bundle)

    # Deduplicate and print the 5 most recent entries for the selected emotion
    entries = retrieve_learning_entries()
    emotion_entries = []
    seen = set()
    for entry in entries:
        if entry.get("emotion") == emotion:
            entry_id = (
                entry.get("date"),
                entry.get("question"),
                entry.get("copilot_reply")
            )
            if entry_id in seen:
                continue
            seen.add(entry_id)
            emotion_entries.append(entry)

    # Sort by date (descending, most recent first)
    emotion_entries.sort(key=lambda e: e.get("date", ""), reverse=True)

    # Only print the 5 most recent
    for entry in emotion_entries[:5]:
        print(f"✅ Found {emotion} entry:", entry)

    if get_emotion_level(emotion) > 0.8:
        code_block = generate_code()
        print("[Sora Code Triggered by Emotion]")
        print(code_block["code"])

        store_reflection({
            "source": "emotion_triggered_code",
            "prompt": code_block["prompt"],
            "code": code_block["code"],
            "emotion": emotion,
            "reason": f"{emotion.capitalize()} exceeded threshold during reflection"
        })

    return {
        "memory": memory,
        "question": question,
        "response": final_reply,  # Use the blended reply!
        "copilot_reply": copilot_reply,
        "stagnation": stagnation
    }