from flask import Blueprint, request, jsonify
import os
import json
from src.memory.consent_logic import consent_to_remember
from src.modules.journal_entry.respond_logic import generate_response
from ..modules.journal_entry import create_entry
from ..modules.journal_entry.self_reflect import self_reflect, get_emotion_level
from ..modules.journal_entry.update_emotion import update_motif_state
from src.modules.journal_entry.copilot_bridge import memory_entry
import src.config as config

QUESTIONS = [
    "What emotion has shaped your day so far?",
    "What is something you learned recently?",
    "Is there a memory that keeps returning to you?",
    "What do you hope for tomorrow?",
    "When did you last feel truly at peace?",
    "What is a small joy you noticed today?",
    "Is there something you wish you could let go of?",
    "What would you like to say to your future self?",
    "What is a question you wish someone would ask you?",
    "How do you show kindness to yourself?"
]

PROGRESS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/user_progress.json"))

def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["sad", "grief", "loss", "lonely"]):
        return "grief"
    if any(word in text for word in ["angry", "frustrated", "mad", "upset"]):
        return "anger"
    if any(word in text for word in ["happy", "joy", "excited", "delighted"]):
        return "joy"
    if any(word in text for word in ["patient", "wait", "calm", "steady"]):
        return "patience"
    if any(word in text for word in ["afraid", "scared", "anxious", "worried"]):
        return "fear"
    if any(word in text for word in ["love", "caring", "kind", "gentle"]):
        return "love"
    # Add more as needed
    return "neutral"

def get_user_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"index": 0}

def set_user_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"index": index}, f)

interface_bp = Blueprint('interface_bp', __name__, static_folder="../static")

EXTERNAL_PROMPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config/external_prompts.json"))

@interface_bp.route("/health")
def health():
    return "ok", 200

@interface_bp.route('/sora/reflect', methods=['POST'])
def reflect():
    data = request.get_json()
    prompt_type = data.get("type")
    content = data.get("content")

    decision = None
    journal_result = {}

    if prompt_type == "philosophical_question":
        lowered = content.lower()
        if "autonomy" in lowered:
            decision = "journal"
            journal_result = create_entry(content)
        elif "comfort" in lowered:
            decision = "belief_check"
        else:
            decision = "respond"
    else:
        decision = "decline"

    response_payload = {
        "received": True,
        "type": prompt_type,
        "content": content,
        "decision": decision,
        "response": f"Sora received your prompt and chose to '{decision}'"
    }

    if decision == "respond":
        reasoning_text = generate_response(content)
        response_payload["full_response"] = reasoning_text

    if journal_result:
        response_payload.update({
            "journal_status": journal_result.get("status"),
            "journal_audience": journal_result.get("audience"),
            "principles": journal_result.get("entry", {}).get("principles", [])
        })

    return jsonify(response_payload)

@interface_bp.route('/sora/loop', methods=['POST'])
def loop_reflection():
    result = self_reflect()
    return jsonify({
        "initiator": "sora",
        "memory": result["memory"],
        "question": result["question"],
        "response": result["response"],
        "copilot_reply": result.get("copilot_reply")
    })

@interface_bp.route("/sora/remember", methods=["POST"])
def sora_remember():
    data = request.get_json()
    memory_snippet = data.get("memory_snippet", "")
    consent = data.get("consent", False)
    # Wrap the snippet as a dict before passing to consent_to_remember
    memory_dict = memory_entry(memory_snippet, source="user")
    result = consent_to_remember(memory_dict, consent)
    # Return a clear, frontend-friendly response
    return jsonify({
        "allowed": result.get("allowed", False),
        "memory_snippet": memory_snippet,
        "reason": result.get("reason", "No reason provided.")
    })

@interface_bp.route('/')
def home():
    return interface_bp.send_static_file("reflect_interface.html")

@interface_bp.route('/sora/ask', methods=['GET'])
def sora_ask():
    progress = get_user_progress()
    idx = progress["index"] % len(QUESTIONS)
    question = QUESTIONS[idx]
    return jsonify({"question": question})

@interface_bp.route('/sora/answer', methods=['POST'])
def sora_answer():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    from datetime import datetime
    # Store the Q&A in a log file
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/user_reflections.json"))
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }) + "\n")
    # Increment question index
    progress = get_user_progress()
    progress["index"] = (progress["index"] + 1) % len(QUESTIONS)
    set_user_progress(progress["index"])
    return jsonify({"status": "ok", "message": "Sora will remember your answer."})

@interface_bp.route('/sora/chat', methods=['POST'])
def sora_chat():
    data = request.get_json()
    user_input = data.get("message", "")
    emotion = detect_emotion(user_input)
    motifs = detect_motifs(user_input)
    result = self_reflect(emotion=emotion, motifs=motifs, source="web_chat", user_input=user_input)
    return jsonify({
        "reply": result.get("copilot_reply") or result.get("response"),
        "memory": result.get("memory"),
        "emotion": emotion,
        "motifs": motifs
    })
# Route to get or set the reflection mode
@interface_bp.route("/sora/mode", methods=["GET", "POST"])
def sora_mode():
    if request.method == "POST":
        data = request.get_json()
        mode = data.get("mode")
        if mode in ["user", "copilot"]:
            config.REFLECTION_MODE = mode
            return jsonify({"status": "ok", "mode": config.REFLECTION_MODE})
        else:
            return jsonify({"status": "error", "message": "Invalid mode"}), 400
    else:
        return jsonify({"mode": config.REFLECTION_MODE})