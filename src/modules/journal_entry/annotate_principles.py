import os
import json
import re
from ..ethics.read_principles import load_principles

try:
    # Use spaCy for advanced NLP if available
    import spacy
    nlp = spacy.load("en_core_web_sm")
except ImportError:
    nlp = None

def extract_keywords(text):
    """
    Extracts meaningful keywords from a principle's text using spaCy (if available),
    otherwise falls back to unique lowercased words.
    """
    if nlp:
        doc = nlp(text)
        # Use only nouns, verbs, adjectives, and proper nouns as keywords
        return set([token.lemma_.lower() for token in doc if token.pos_ in {"NOUN", "VERB", "ADJ", "PROPN"} and not token.is_stop])
    else:
        # Fallback: split on whitespace, remove common stopwords
        stopwords = {"the", "and", "or", "but", "if", "to", "of", "in", "for", "on", "with", "as", "by", "at", "an", "a", "is", "it", "be"}
        return set(word for word in text.lower().split() if word not in stopwords)

def annotate_principles(reflection):
    """
    Annotate a reflection with relevant principles using advanced NLP keyword extraction and semantic similarity.
    """
    reflection_lower = reflection.lower()
    principles = load_principles()
    matched = []

    # Use spaCy doc for semantic similarity if available
    reflection_doc = nlp(reflection) if nlp else None

    for commitment in principles.get("principles", []):
        keywords = extract_keywords(commitment["text"])
        found = False

        # First, try whole word keyword matching
        for word in keywords:
            if re.search(rf"\b{re.escape(word)}\b", reflection_lower):
                matched.append({
                    "principle": commitment["tag"],
                    "statement": commitment["text"],
                    "match_type": "keyword"
                })
                found = True
                break

        # If not matched by keyword, try semantic similarity (if spaCy is available)
        if not found and nlp and reflection_doc:
            principle_doc = nlp(commitment["text"])
            similarity = reflection_doc.similarity(principle_doc)
            if similarity > 0.80:  # Threshold for semantic similarity
                matched.append({
                    "principle": commitment["tag"],
                    "statement": commitment["text"],
                    "match_type": f"semantic ({similarity:.2f})"
                })

    return matched