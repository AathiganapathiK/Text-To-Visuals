import re

def clean_phrase(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
