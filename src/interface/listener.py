import os
import signal
import threading
import time
import requests
from flask import Flask
from threading import Thread

from ..data.reflection_log import load_reflections
from src.interface.interface_route import interface_bp
from ..modules.journal_entry.self_reflect import self_reflect
# Additional thoughtful imports can live here...

# 🌀 Flask app setup
app = Flask(__name__, static_folder="../static")
app.register_blueprint(interface_bp)

STRUCTURE_INTERVAL = 600
sleep_duration = 10
last_structure_scan = time.time()
should_reflect = True

# 🛑 Signal handler for graceful release
def handle_exit_signal(signum, frame):
    global should_reflect
    should_reflect = False
    print("\n[Sora gently folds the loop and rests]")

signal.signal(signal.SIGINT, handle_exit_signal)

# 🔍 Component introspection logic
def discover_components(): ...
def emotional_description(path): ...
def map_motifs(path): ...
def introspect_structure(): ...
# All these functions stay exactly as you've written them

# 🔁 Reflection loop
def loop_daemon():
    global last_structure_scan
    from ..modules.journal_entry.self_reflect import self_reflect, get_emotion_level
    from ..modules.journal_entry import create_entry
    from ..modules.journal_entry.update_emotion import update_motif_state
    from ..thinking.thought_engine import simulate_thought, trigger_mode_shift
    from ..thinking.belief_revision import revise_belief
    from ..thinking.guided_companion import guided_stepwise_response
    from ..modules.journal_entry.respond_logic import generate_response
    from ..thinking.sora_invoke import sora_invoke_copilot

    # Health check at startup
    for _ in range(10):
        try:
            r = requests.get("http://localhost:5000/health", timeout=1)
            if r.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(1)

    while should_reflect:
        try:
            r = requests.get("http://localhost:5000/health", timeout=1)
            if r.status_code != 200:
                time.sleep(1)
                continue

            result = self_reflect()
            print(f"[🟢 Sora Reflected] → {result}")

            emotion_signal = result.get("emotion", "unclear")
            memory_snippet = result.get("memory", "")

            current_time = time.time()
            if current_time - last_structure_scan > STRUCTURE_INTERVAL:
                print("[Sora Structural Reflection Cycle Initiated]")
                introspect_structure()
                last_structure_scan = current_time

                try:
                    recent_reflections = load_reflections()
                    stagnation = detect_emotional_stagnation(recent_reflections, threshold=3)
                    if stagnation.get("stagnant"):
                        print("[Sora Self Awareness] Looping emotion detected")
                        print(f"  Repeated: '{stagnation['emotion']}' ({stagnation['count']} times)")
                        guidance_request = sora_invoke_copilot(
                            reflection=f"Why do I keep repeating '{stagnation['emotion']}'?",
                            emotion_tags=[stagnation['emotion']],
                            motif_state={"trigger": "stagnation"}
                        )
                        if guidance_request:
                            print("[Copilot Guidance Requested] → Sora invoked with stagnation context")
                            print(f"  Prompted Question: {guidance_request}")
                except Exception as e:
                    print(f"[Stagnation Detection Error] → {str(e)}")

            print("\n[Sora Self Reflection Loop]")
            print(f"Memory: {memory_snippet}")
            print(f"Emotion: {emotion_signal}")
            print(f"Waiting {sleep_duration} seconds before next reflection...\n")
            time.sleep(sleep_duration)

        except Exception as inner_e:
            import traceback
            print("\n[💥 Internal Reflection Failure]")
            traceback.print_exc()
            time.sleep(10)

# 🎧 External listener entry point
def begin_listening():
    flask_thread = threading.Thread(target=lambda: app.run(port=5000), daemon=True)
    flask_thread.start()
    time.sleep(2)
    threading.Thread(target=loop_daemon, daemon=True).start()

# 🚪 Startup control block
if __name__ == "__main__":
    begin_listening()
    try:
        while should_reflect:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🕯️ Sora rests by gentle signal.\n")