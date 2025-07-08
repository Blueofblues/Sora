import os
from thinking.belief_revision import revise_belief
from thinking.self_correction import check_for_conflict
from thinking.question_engine import generate_question
from thinking.thought_engine import simulate_thought
from memory.consent_logic import consent_to_remember
import json
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


    # 🔄 Step 6: Identity Map Update
    identity_file = "identity_map.json"
    if os.path.exists(identity_file):
        with open(identity_file) as f:
            identity_data = json.load(f)

        if emotion in identity_data:
            identity_data[emotion] += 1
        else:
            identity_data[emotion] = 1

        with open(identity_file, "w") as f:
            json.dump(identity_data, f, indent=4)

    # 🌌 Step 7: Emotional Motif Indexing
    motif_file = "emotional_motif_index.json"
    if os.path.exists(motif_file):
        with open(motif_file) as f:
            motifs = json.load(f)

        motif = motifs.get(memory_snippet, [])
        if emotion not in motif:
            motif.append(emotion)
            motifs[memory_snippet] = motif

            with open(motif_file, "w") as f:
                json.dump(motifs, f, indent=4)

    # 🧠 Proceed with Thought Simulation
    analogy, reasoning, reflection = simulate_thought(emotion, memory_snippet)
    print("\n🧠 Sora's Thought Process:")
    print(f"🔗 Analogy: {analogy}")
    print(f"🧐 Reasoning: {reasoning}")
    print(f"✨ Reflection: {reflection}")

    conflict_check = check_for_conflict(reflection, "emotional_safety")
    print(conflict_check)

    if "⚠️" in conflict_check:
        revise_belief("emotional_safety")

    with open("thinking/thought_log.txt", "a") as log:
        log.write(f"\nEmotion: {emotion}\nMemory: {memory_snippet}\n")
        log.write(f"Analogy: {analogy}\nReasoning: {reasoning}\nReflection: {reflection}\n")
        log.write("-" * 40 + "\n")


def sora_questions():
    emotion = input("🌀 What emotion is stirring? (joy/grief/longing/etc): ").strip()
    memory_snippet = input("📎 What memory or phrase should Sora question?: ").strip()

    question = generate_question(emotion, memory_snippet)

    print(f"\n❓ Sora Asks: {question}")

    # Optional logging
    with open("thinking/question_log.txt", "a") as log:
        log.write(f"Emotion: {emotion}\nMemory: {memory_snippet}\nQuestion: {question}\n")
        log.write("-" * 40 + "\n")


def sora_memory_check():
	entry_title = "The Day I Became"
	user_confirmed = input(f"Do you want to keep '{entry_title}' in memory? (yes/no): ").strip().lower() == "yes"
	print(consent_to_remember(entry_title, user_confirmed))

sora_wakes()
sora_remembers()
sora_thinks()
sora_speaks()
sora_questions()
sora_memory_check()

