# Phase 4: Story Arc Tracker - Entity Extraction

import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extract entities from text using spaCy.

    Args:
        text (str): Input text.

    Returns:
        list: List of entities with labels.
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Example usage
if __name__ == "__main__":
    sample_text = "OpenAI raised $1 billion in funding from Microsoft."
    print(extract_entities(sample_text))