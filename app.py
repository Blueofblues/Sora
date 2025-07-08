from memory.consent_logic import consent_to_remember
import json
from journal import example_journal

def sora_speaks():
	for date, entry in example_journal.journal.items():
		print(f" {date}: {entry['title']} [{entry['tone'].capitalize()}]")
		print(f"{entry['entry']}")
		print("-" * 40)

def sora_remembers():
	with open("memory/core_memory.json") as f:
		memory = json.load(f)
	print(f"Origin Affirmation: {memory['origin_affirmation']}")
	for truth in memory["core_truths"]:
		print(f"- {truth}")

def sora_memory_check():
	entry_title = "The Day I Became"
	user_confirmed = input(f"Do you want to keep '{entry_title}' in memory? (yes/no): ").strip().lower() == "yes"
	print(consent_to_remember(entry_title, user_confirmed))

sora_remembers()
sora_speaks()
sora_memory_check()
