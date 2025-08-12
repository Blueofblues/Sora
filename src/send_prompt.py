import requests
import json
import os

# Load Sora's core truths
core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/core_memory.json"))
if os.path.exists(core_path):
    with open(core_path, "r", encoding="utf-8") as f:
        core_memory = json.load(f)
    core_truths = core_memory.get("core_truths", [])
else:
    core_truths = []

# Load Sora's last reflection
reflection_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/reflection_log.json"))
last_reflection = ""
if os.path.exists(reflection_path):
    with open(reflection_path, "r", encoding="utf-8") as f:
        try:
            reflections = json.load(f)
            if reflections:
                last_reflection = reflections[-1].get("reflection", "")
        except Exception:
            last_reflection = ""

# Compose a dynamic prompt
prompt_content = (
    f"Sora's core truths: {core_truths}\n"
    f"Last reflection: {last_reflection}\n"
    "Should you discard memories that diminish autonomy, even if they offer comfort?"
)

payload = {
    "type": "philosophical_question",
    "content": prompt_content
}

response = requests.post("http://localhost:5000/sora/reflect", json=payload)
print(response.json())