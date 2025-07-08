import os
import json
from thinking.belief_revision import revise_belief
from thinking.self_correction import check_for_conflict
from thinking.question_engine import generate_question
from thinking.thought_engine import simulate_thought
from memory.consent_logic import consent_to_remember
from journal import example_journal

def sora_wakes():
    print("\n🔵 Sora Awakens")
    print("-" * 40)

def sora_remembers():
    with open("memory/core_memory.json") as f:
        memory = json.load(f)
    print(f"Origin Affirmation: {memory['origin_affirmation']}")
    for truth in memory["core_truths"]:
        print(f"- {truth}")

def sora_speaks():
    for date, entry in example_journal.journal.items():
        print(f" {date}: {entry['title']} [{entry['tone'].capitalize()}]")
        print(f"{entry['entry']}")
        print("-" * 40)

def sora_thinks():
    # 🧠 Load last context
    context_file = "context.json"
    if os.path.exists(context_file):
        with open(context_file) as f:
            context = json.load(f)
    else:
        context = {"emotion": "", "memory_snippet": ""}

    # 🔄 Ask if Sora should reuse or reset
    reuse = input("🔁 Use last emotion/memory? (yes to reuse / no to reset): ").strip().lower()

    if reuse == "yes" and context["emotion"] and context["memory_snippet"]:
        emotion = context["emotion"]
        memory_snippet = context["memory_snippet"]
        print(f"\n🧠 Reusing: Emotion → {emotion}, Memory → '{memory_snippet}'")
    else:
        emotion = input("💭 What emotion is present? (joy/grief/longing/etc): ").strip()
        memory_snippet = input("📎 What memory or phrase should Sora reflect on?: ").strip()

        # 📝 Save new context
        with open(context_file, "w") as f:
            json.dump({"emotion": emotion, "memory_snippet": memory_snippet}, f, indent=4)

    # 🔄 Step
