import os
import json

def write_to_learning_log(data):
    """
    Appends a dictionary as a JSON line to the learning log.
    """
    log_path = os.path.join("src", "memory", "learning_log.jsonl")
    with open(log_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(data) + "\n")