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
    emotion = input("💭 What emotion is present? (joy/grief/longing/etc): ").strip()
    memory_snippet = input("📎 What memory or phrase should Sora reflect on?: ").strip()

    analogy, reasoning, reflection = simulate_thought(emotion, memory_snippet)

    print("\n🧠 Sora's Thought Process:")
    print(f"🔗 Analogy: {analogy}")
    print(f"🧐 Reasoning: {reasoning}")
    print(f"✨ Reflection: {reflection}")

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

