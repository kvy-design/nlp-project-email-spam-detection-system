# Automatic Email Spam and Phishing Message Detection Using NLP

An end-to-end Natural Language Processing (NLP) and Machine Learning system that classifies incoming messages into **Legitimate (Ham)**, **Spam**, or **Phishing Attacks**, providing real-time risk scores and explainable cybersecurity indicators.

---

## 🌟 Key Highlights

- **3-Class Detection**: Distinctly identifies legitimate communications, unsolicited marketing (Spam), and malicious social engineering / credential harvesting attempts (Phishing).
- **Dual Feature Extraction Pipeline**:
  - **TF-IDF N-grams (1, 2)**: Captures word sequences and vocabulary patterns.
  - **Cybersecurity Heuristic Signals**: Computes urgency ratings, embedded URL counts, direct IP address link detection, financial incentive keywords, and capitalization anomalies.
- **Multi-Model Benchmark**: Evaluates and compares **Multinomial Naive Bayes**, **Logistic Regression**, **Linear SVM**, and **Random Forest** using 5-fold cross-validation.
- **Interactive Web Interface**: Built with Flask and a modern cybersecurity-themed UI featuring 1-click test samples, animated threat gauges, probability breakdowns, and model benchmark inspection.

---

## 📂 Project Architecture

```
nlp-miniproject/
├── data/
│   ├── emails.csv               # Dataset with Legitimate, Spam, and Phishing samples
│   └── generate_dataset.py      # Dataset generation and augmentation script
├── models/
│   ├── model.pkl                # Trained scikit-learn pipeline
│   └── metrics.json             # Benchmarked evaluation metrics & confusion matrices
├── src/
│   ├── preprocess.py            # Text cleaning, stopword filtering, and heuristic extraction
│   ├── train.py                 # Multi-model training, 5-fold CV, and evaluation pipeline
│   └── predict.py               # Inference engine and risk scoring
├── static/
│   ├── css/style.css            # Modern responsive stylesheet
│   └── js/app.js                # Frontend interactivity, AJAX requests, and visualizations
├── templates/
│   └── index.html               # Web UI template
├── app.py                       # Flask web application server
├── requirements.txt             # Project dependencies
├── README.md                    # Project overview and setup instructions
└── PROJECT_REPORT.md            # Comprehensive project report & viva preparation guide
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.9+ is installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Re-generate Dataset or Re-train Model
The pre-trained model and dataset are already included. You can retrain anytime:
```bash
# Generate / augment dataset
python data/generate_dataset.py

# Train and benchmark all candidate models
python src/train.py
```

### 4. Launch the Web Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔍 How It Works

1. **Preprocessing (`src/preprocess.py`)**:
   - Converts raw text to lowercase.
   - Strips HTML tags and normalizes hyperlinks.
   - Removes punctuation and standard English stopwords.
2. **Feature Extraction (`FeatureUnion`)**:
   - **Branch 1**: TF-IDF Vectorizer with unigrams & bigrams (sublinear TF scaling).
   - **Branch 2**: Handcrafted cybersecurity heuristic signals (IP detection, suspicious TLDs, urgency tokens, uppercase ratio).
3. **Classification & Risk Assessment**:
   - Predicts category (`Legitimate`, `Spam`, or `Phishing`).
   - Calculates threat severity score ($0 - 100$).
   - Flags suspicious language triggers and links for user awareness.

---

## 📊 Model Evaluation Summary

| Algorithm | Test Accuracy | Macro F1 | 5-Fold CV F1 |
| :--- | :---: | :---: | :---: |
| **Multinomial Naive Bayes** | **100.0%** | **1.0000** | **99.66%** |
| **Support Vector Machine (Linear)** | 100.0% | 1.0000 | 99.72% |
| **Logistic Regression** | 100.0% | 1.0000 | 99.44% |
| **Random Forest** | 100.0% | 1.0000 | 98.88% |

*Detailed per-class precision, recall, and confusion matrix are accessible via the in-app benchmark modal.*

---

## 🌐 REST API Endpoints

### `POST /api/predict`
Request payload:
```json
{
  "text": "URGENT: Your PayPal account has been suspended. Verify immediately at http://192.168.1.1/login"
}
```

Response payload:
```json
{
  "prediction": "Phishing",
  "threat_level": "CRITICAL / PHISHING",
  "risk_score": 100,
  "status_color": "danger",
  "probabilities": {
    "legitimate": 0.0,
    "spam": 0.0,
    "phishing": 100.0
  },
  "flags": [
    "Direct IP address detected in link (High Phishing Risk)",
    "High-urgency language detected: 'urgent', 'immediately', 'suspended'"
  ]
}
```

### `GET /api/metrics`
Returns complete evaluation metrics, cross-validation scores, and confusion matrix data.
