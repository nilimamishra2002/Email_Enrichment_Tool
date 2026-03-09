import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"[^a-z\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


sector_descriptions = {

    "IT Services":
    "software technology digital transformation cloud computing "
    "cybersecurity data analytics artificial intelligence IT consulting "
    "enterprise solutions platform engineering services",

    "E-Commerce":
    "online shopping marketplace digital retail ecommerce "
    "product listings payment checkout logistics delivery customers",

    "Financial Services":
    "banking finance financial services fintech investment "
    "insurance wealth management capital markets payments",

    "Healthcare":
    "healthcare hospital medical services pharmaceuticals "
    "biotechnology clinical research patient care health systems",

    "Manufacturing":
    "manufacturing industrial production factories machinery "
    "engineering production plants industrial equipment",

    "Energy":
    "energy power generation electricity renewable energy "
    "solar wind oil gas utilities power plants",

    "Education":
    "education university learning training academic programs "
    "research institutions students curriculum",

    "Telecommunications":
    "telecommunications telecom mobile networks broadband "
    "5g connectivity communication infrastructure",

    "Transportation":
    "transport logistics shipping freight supply chain "
    "delivery networks cargo transport mobility",

    "Aerospace": [
    "aircraft","aviation","aerospace","defense","flight","airplanes"
]
}


def classify_sector(text):

    # Safety: ensure text is always a string
    if isinstance(text, list):
        text = " ".join(str(x) for x in text)

    if not isinstance(text, str):
        text = str(text)

    text = clean_text(text)

    if not text:
        return "Unknown", 0

    sectors = list(sector_descriptions.keys())

    corpus = [str(text)] + [str(v) for v in sector_descriptions.values()]

    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    best_index = similarities.argmax()

    best_sector = sectors[best_index]

    best_score = float(similarities[best_index])

    if best_score < 0.05:
        return "Unknown", best_score

    return best_sector, best_score