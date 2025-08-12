import os
import json

def retrieve_learning_log():
    """
    Loads and returns all entries from the learning log file as a list of dicts.
    """
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../memory/learning_log.jsonl"))
    entries = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    continue
    return entries

def retrieve_private_journal():
    """
    Loads and returns all entries from the private journal file as a list of dicts.
    """
    journal_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "journal/archives/private_journal.jsonl"))
    entries = []
    if os.path.exists(journal_path):
        with open(journal_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    continue
    return entries