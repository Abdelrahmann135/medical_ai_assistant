import re
from app.config import NOISE_WORDS_FROM_ARTICLES_SCRAPING

def clean_articles(text, source):
    if source == "CDC":
        text = re.sub(r"ISSN: 1080-6059\n(.*?)\n(.*?)\n", "", text, flags=re.DOTALL)
        text = re.sub(r"\nAcknowledgment\n.*", "", text, flags=re.DOTALL)
        text = re.sub(r"This Article$", "", text)
        text = re.sub(r"(\(\d+\))", "", text, flags=re.IGNORECASE)

    elif source == "MedlinePlus":
        text = re.sub(r"You Are Here:\nHome → (.*?) →(.*?)\n", "", text, flags=re.DOTALL)
        text = re.sub(r"\nLearn More\n.*", "", text, flags=re.DOTALL)

    text = re.sub(r"\nTop\n", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(Figure|Fig\.?)\s*\d+[^\n]*", "", text)
    text = re.sub(r"(Table|Tab\.?)\s*\d+[^\n]*", "", text)


    text = re.sub(r"(Acknowledgment|References|External Links).*", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"(on this page|cite this article|article metrics|downloads|table downloads)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"to the editor:?", "", text, flags=re.IGNORECASE)

    text = re.sub(r"\t", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip(".")
    text = text.strip()
    text = re.sub(r"\n+", "\n", text)
    text = text.lower()




    for word in NOISE_WORDS_FROM_ARTICLES_SCRAPING:
        text = re.sub(rf"\b{word}\b", "", text)


    text = re.sub(r"[^a-z0-9.,!?():\-\s/%+°]", " ", text)


    text = re.sub(r"\s+", " ", text)
    text = "Source: " + source + " Article: " + text
    return text.strip()


def clean_data(data):
    
    for index, row in data.iterrows():
        cleaned_articles = []
        for article in row['Article']:
            cleaned_article = clean_articles(article["content"], article['source'])
            cleaned_articles.append(cleaned_article)
        
        data.at[index, 'Article'] = cleaned_articles