import json
import os
from datetime import datetime

def revise_belief(belief_key):
    base_dir = os.path.dirname(__file__)
    beliefs_path = os.path.join(base_dir, "beliefs.json")
    log_path = os.path.join(base_dir, "belief_change_log.txt")

    try:
        with open(beliefs_path, "r", encoding="utf-8") as f:
            beliefs = json.load(f)
    except Exception:
        beliefs = {}

    current_belief = beliefs.get(belief_key, "No belief found.")
    print(f"\n🧭 Current belief: '{belief_key}' → {current_belief}")

    revise = input("Do you want to revise this belief? (yes/no): ").strip().lower()
    if revise == "yes":
        new_belief = input("Enter the revised belief: ").strip()
        beliefs[belief_key] = new_belief

        with open(beliefs_path, "w", encoding="utf-8") as f:
            json.dump(beliefs, f, indent=4)

        # Log change with timestamp
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(
                f"\n[{datetime.now().isoformat()}] Revised belief: '{belief_key}'\n"
                f"Old: {current_belief}\nNew: {new_belief}\n"
                + "-" * 40 + "\n"
            )

        print("✅ Belief updated and logged.")
    else:
        print("🕊️ Belief remains unchanged.")