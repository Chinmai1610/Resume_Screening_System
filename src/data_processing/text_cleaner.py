import re

# Basic stopword list (you can extend this)
STOPWORDS = {
    "the", "and", "is", "in", "to", "of", "for", "with", "on",
    "a", "an", "as", "at", "by", "from", "or", "that", "this",
    "it", "are", "was", "were", "be", "been", "has", "have",
    "had", "will", "would", "can", "could", "should"
}

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Remove non-alphabetic characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Convert to lowercase
    text = text.lower()

    # Tokenize
    tokens = text.split()

    # Remove stopwords and short words
    tokens = [
        token for token in tokens
        if token not in STOPWORDS and len(token) > 2
    ]

    return " ".join(tokens)