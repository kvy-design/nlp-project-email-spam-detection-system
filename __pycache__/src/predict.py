import os
import sys
import joblib
import numpy as np

# Ensure src in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocess import CleanTextTransformer, HeuristicFeatureExtractor, extract_cyber_features

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "model.pkl")

_cached_model = None

def get_model():
    global _cached_model
    if _cached_model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run src/train.py first!")
        _cached_model = joblib.load(MODEL_PATH)
    return _cached_model

def analyze_message(text: str) -> dict:
    """Performs end-to-end NLP classification and cybersecurity risk assessment."""
    if not text or not text.strip():
        return {
            "error": "Empty message provided.",
            "category": "Unknown",
            "risk_score": 0,
            "threat_level": "Safe"
        }
        
    model_bundle = get_model()
    pipeline = model_bundle["pipeline"]
    classes = model_bundle["classes"]
    
    # 1. Feature heuristics extraction
    heuristics = extract_cyber_features(text)
    
    # 2. Model prediction & probabilities
    prediction = pipeline.predict([text])[0]
    
    # Get probabilities if supported
    probs = {}
    if hasattr(pipeline, "predict_proba"):
        raw_probs = pipeline.predict_proba([text])[0]
        for idx, cls in enumerate(pipeline.classes_):
            probs[str(cls)] = float(np.round(raw_probs[idx] * 100, 2))
    else:
        probs = {str(c): (100.0 if str(c) == str(prediction) else 0.0) for c in classes}
        
    # 3. Formulate explainable risk flags
    flags = []
    
    if heuristics["has_ip_url"]:
        flags.append("Direct IP address detected in link (High Phishing Risk)")
    if heuristics["suspicious_domain_count"] > 0:
        flags.append(f"Suspicious top-level domain or auth keyword detected ({heuristics['suspicious_domain_count']} match)")
    if heuristics["urgency_score"] > 0:
        hits = ", ".join(f"'{w}'" for w in heuristics["urgency_hits"][:3])
        flags.append(f"High-urgency language detected: {hits}")
    if heuristics["financial_score"] > 0:
        hits = ", ".join(f"'{w}'" for w in heuristics["financial_hits"][:3])
        flags.append(f"Financial / monetary incentives detected: {hits}")
    if heuristics["upper_ratio"] > 0.25 and len(text) > 20:
        flags.append(f"Abnormally high uppercase text ratio ({int(heuristics['upper_ratio']*100)}%)")
    if heuristics["exclamation_count"] >= 3:
        flags.append(f"Excessive exclamation marks ({heuristics['exclamation_count']})")
    if heuristics["url_count"] >= 2:
        flags.append(f"Multiple external hyperlinks embedded ({heuristics['url_count']} URLs)")

    # 4. Determine overall risk score (0-100) and threat badge
    phishing_prob = probs.get("phishing", 0.0)
    spam_prob = probs.get("spam", 0.0)
    
    if prediction == "phishing":
        risk_score = max(int(phishing_prob), 80)
        threat_level = "CRITICAL / PHISHING"
        status_color = "danger"
    elif prediction == "spam":
        risk_score = max(int(spam_prob * 0.7), 45)
        threat_level = "MODERATE / SPAM"
        status_color = "warning"
    else:
        # Legitimate
        risk_score = min(int((100 - probs.get("legitimate", 95)) * 0.5), 20)
        threat_level = "SAFE / LEGITIMATE"
        status_color = "success"
        
    return {
        "prediction": prediction.capitalize(),
        "threat_level": threat_level,
        "status_color": status_color,
        "risk_score": risk_score,
        "probabilities": probs,
        "flags": flags,
        "heuristics": heuristics,
        "best_model_used": model_bundle.get("best_model_name", "Naive Bayes")
    }

if __name__ == "__main__":
    test_email = (
        "URGENT: Your PayPal account has been temporarily restricted due to unauthorized login attempts. "
        "Verify your identity immediately at http://192.168.1.10/paypal-verify or your account will be deleted."
    )
    res = analyze_message(test_email)
    print("Test Prediction:")
    print(res)
