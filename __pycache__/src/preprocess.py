import re
import string
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Standard English stopwords to avoid external download dependencies
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
    "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
    "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
    "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom",
    "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
    "your", "yours", "yourself", "yourselves"
}

URGENT_WORDS = [
    "urgent", "immediately", "immediate", "suspended", "restricted", "expire", "expires",
    "warning", "action required", "critical", "freeze", "locked", "unauthorized",
    "termination", "deactivated", "final notice", "confirm identity", "verify your"
]

FINANCIAL_WORDS = [
    "winner", "won", "prize", "cash", "bonus", "free", "discount", "refund", "dollar",
    "dollars", "claim", "invest", "investment", "bitcoin", "crypto", "jackpot", "lottery",
    "earn", "loan", "rich", "credit card", "millionaire"
]

SUSPICIOUS_DOMAINS = [
    ".xyz", ".top", ".cc", ".site", ".info", ".biz", "-verify", "-security", "-login",
    "-portal", "-support", "-update", "restore", "auth", "dispatch"
]

def clean_text(text: str) -> str:
    """Preprocesses raw text: strips HTML, URLs, non-alphanumeric, and stopwords."""
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    cleaned = text.lower()
    
    # 2. Remove HTML tags
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    
    # 3. Replace URLs and IP addresses with a token placeholder
    cleaned = re.sub(r"https?://\S+|www\.\S+", " urltoken ", cleaned)
    
    # 4. Remove special characters and punctuation
    cleaned = re.sub(r"[^a-zA-Z\s]", " ", cleaned)
    
    # 5. Tokenize and remove stopwords
    tokens = cleaned.split()
    tokens = [t for t in tokens if len(t) > 2 and t not in STOPWORDS]
    
    return " ".join(tokens)


def extract_cyber_features(text: str) -> dict:
    """Extracts interpretable cybersecurity heuristic signals from raw email text."""
    if not isinstance(text, str):
        text = ""
        
    length = len(text) if len(text) > 0 else 1
    lower_text = text.lower()
    
    # 1. URL Analysis
    urls = re.findall(r"https?://\S+|www\.\S+", text, re.IGNORECASE)
    url_count = len(urls)
    
    has_ip_url = int(bool(re.search(r"https?://(?:\d{1,3}\.){3}\d{1,3}", text)))
    
    suspicious_domain_count = sum(
        1 for d in SUSPICIOUS_DOMAINS if d in lower_text
    )
    
    # 2. Urgency and Threat Language
    urgency_hits = [w for w in URGENT_WORDS if w in lower_text]
    urgency_score = len(urgency_hits)
    
    # 3. Financial and Promotional Language
    financial_hits = [w for w in FINANCIAL_WORDS if w in lower_text]
    financial_score = len(financial_hits)
    
    # 4. Structural Markers
    exclamation_count = text.count("!")
    dollar_count = text.count("$")
    upper_count = sum(1 for c in text if c.isupper())
    upper_ratio = upper_count / length
    
    return {
        "url_count": url_count,
        "has_ip_url": has_ip_url,
        "suspicious_domain_count": suspicious_domain_count,
        "urgency_score": urgency_score,
        "financial_score": financial_score,
        "exclamation_count": exclamation_count,
        "dollar_count": dollar_count,
        "upper_ratio": upper_ratio,
        "urgency_hits": urgency_hits,
        "financial_hits": financial_hits
    }


class CleanTextTransformer(BaseEstimator, TransformerMixin):
    """Sklearn compatible transformer that cleans raw text messages."""
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        return [clean_text(x) for x in X]


class HeuristicFeatureExtractor(BaseEstimator, TransformerMixin):
    """Sklearn compatible transformer that extracts numerical heuristic features."""
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        features = []
        for text in X:
            f = extract_cyber_features(text)
            features.append([
                f["url_count"],
                f["has_ip_url"],
                f["suspicious_domain_count"],
                f["urgency_score"],
                f["financial_score"],
                f["exclamation_count"],
                f["dollar_count"],
                f["upper_ratio"]
            ])
        return np.array(features, dtype=float)
