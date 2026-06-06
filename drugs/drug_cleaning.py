import re
from bs4 import BeautifulSoup


def clean_drug_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9.,;:%()\-\\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    sentences = text.split(".")
    seen = set()
    cleaned = []

    for s in sentences:
        s = s.strip()
        if s and s.lower() not in seen:
            seen.add(s.lower())
            cleaned.append(s)

    return ". ".join(cleaned)