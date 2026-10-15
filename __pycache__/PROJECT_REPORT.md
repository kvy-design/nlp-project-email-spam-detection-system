# Project Report: Automatic Email Spam and Phishing Message Detection Using NLP

---

## 1. Abstract
Electronic mail and messaging platforms remain the primary communication backbone for academic, personal, and corporate interactions. Concurrently, they represent the single largest attack vector for social engineering, unsolicited marketing (spam), and credential theft (phishing). This project presents an end-to-end Natural Language Processing (NLP) and Machine Learning framework capable of classifying incoming messages into three distinct categories: **Legitimate (Ham)**, **Spam**, and **Phishing**. By combining statistical n-gram Term Frequency-Inverse Document Frequency (TF-IDF) feature representations with domain-specific cybersecurity heuristics (IP detection in URLs, urgency markers, and financial lures), the system achieves over 99% cross-validation accuracy. A responsive web application provides real-time classification, dynamic risk severity scoring, and interpretable threat explanations.

---

## 2. Problem Statement & Motivation
Most conventional email filtering systems treat message filtering as a simple binary classification problem (**Spam vs. Ham**). However:
- **Spam** is typically commercial, non-targeted, and designed to advertise products or services. While inconvenient, it generally does not directly threaten account security.
- **Phishing** specifically exploits psychological triggers (urgency, fear, authority) and deceptive technical signals (spoofed links, obfuscated URLs, direct IP destinations) to harvest credentials, banking details, or deliver malware.

Treating phishing merely as generic spam underestimates its severe security risks. A 3-class detection system enables tailored mitigation actions, such as immediate account protection alerts and link blocking for phishing, versus silent routing to a junk folder for spam.

---

## 3. System Architecture & Methodology

```
+-------------------------------------------------------------------------+
|                              Raw Input Message                          |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        NLP Preprocessing Layer                          |
|  - HTML Tag Removal          - Punctuation & Noise Filtering            |
|  - Case Normalization        - Stopword Removal                         |
|  - URL Pattern Extraction    - Tokenization                             |
+-------------------------------------------------------------------------+
                                     |
                 +-------------------+-------------------+
                 |                                       |
                 v                                       v
+----------------------------------+   +----------------------------------+
|      Branch 1: TF-IDF N-Grams    |   |    Branch 2: Cyber Heuristics    |
|  - Unigrams & Bigrams (1, 2)     |   |  - Direct IP in URL Detection    |
|  - Sublinear Term Frequency      |   |  - Urgency Linguistic Score      |
|  - Vocabulary Size: 3,000 terms  |   |  - Suspicious TLD / Auth Tokens  |
|                                  |   |  - Financial Bait Frequency      |
|                                  |   |  - Upper-case Character Ratio    |
+----------------------------------+   +----------------------------------+
                 |                                       |
                 +-------------------+-------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  Feature Union & Feature Vector Assembly                |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                     Multi-Class ML Classification Engine                 |
|  - Multinomial Naive Bayes (Primary)  - Logistic Regression             |
|  - Support Vector Classifier (Linear) - Random Forest Classifier        |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        Output & Interpretability Layer                  |
|  - Predicted Category: Legitimate | Spam | Phishing                     |
|  - Calibrated Confidence Probabilities                                  |
|  - Risk Severity Score (0 to 100)                                       |
|  - Explainable Security Flags (Highlighted trigger keywords & links)    |
+-------------------------------------------------------------------------+
```

---

## 4. Machine Learning Algorithms Implemented

1. **Multinomial Naive Bayes (MNB)**:
   - Uses Bayes' Theorem under the conditional independence assumption.
   - Exceptionally fast, computationally lightweight, and mathematically well-suited for high-dimensional sparse text vectors.
   - Formula:
     $$P(C_k \mid x) \propto P(C_k) \prod_{i=1}^n P(x_i \mid C_k)$$

2. **Logistic Regression (L2 Regularized)**:
   - Fits a multinomial log-odds model using the cross-entropy loss function.
   - Offers well-calibrated posterior probability estimates across classes.

3. **Linear Support Vector Machine (LinearSVC)**:
   - Maximizes the geometric margin between class boundaries in the high-dimensional TF-IDF space.
   - Calibrated using Platt Scaling (`CalibratedClassifierCV`) to output valid probability distributions.

4. **Random Forest Classifier**:
   - An ensemble of decision trees utilizing bootstrap aggregating (bagging) and random feature subsets to capture non-linear interactions between heuristic indicators and keyword frequencies.

---

## 5. Experimental Evaluation & Results

The system was evaluated using an 80/20 stratified split and 5-fold cross-validation.

### 5.1 Model Comparison Table

| Algorithm | Test Accuracy | Macro F1-Score | Weighted F1-Score | 5-Fold CV Macro F1 |
| :--- | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes** | **100.0%** | **1.0000** | **1.0000** | **0.9966 (±0.0068)** |
| **Support Vector Machine (Linear)** | **100.0%** | **1.0000** | **1.0000** | **0.9972 (±0.0056)** |
| **Logistic Regression** | **100.0%** | **1.0000** | **1.0000** | **0.9944 (±0.0069)** |
| **Random Forest** | **100.0%** | **1.0000** | **1.0000** | **0.9888 (±0.0105)** |

### 5.2 Confusion Matrix (Multinomial Naive Bayes)

| Actual \ Predicted | Legitimate (Ham) | Phishing | Spam |
| :--- | :---: | :---: | :---: |
| **Legitimate** | **32** | 0 | 0 |
| **Phishing** | 0 | **20** | 0 |
| **Spam** | 0 | 0 | **28** |

*Result: Zero false positives and zero false negatives on the held-out test set.*

---

## 6. Key Viva & Oral Examination Questions & Answers

### Q1: What is the main difference between Spam and Phishing?
**Answer**: Spam refers to unsolicited bulk electronic messages primarily intended for commercial advertising or nuisance. Phishing is an active social engineering attack where malicious actors impersonate trusted organizations (banks, cloud providers, IT admins) to deceive the recipient into surrendering sensitive credentials, financial data, or downloading malware.

### Q2: Why did you use TF-IDF rather than simple Bag of Words (CountVectorizer)?
**Answer**: Simple Bag of Words only counts raw term frequency, meaning common words can dominate the representation even after basic stopword removal. TF-IDF penalizes words that appear ubiquitously across all documents via Inverse Document Frequency, emphasizing rare, highly discriminative keywords (such as specific banking terms or scam phrases) that characterize individual categories.

### Q3: Why is n-gram range `(1, 2)` better than unigrams alone?
**Answer**: Unigrams only capture individual isolated words. Bigrams preserve context and pairs of words that carry strong semantic meaning, such as *"verify account"*, *"free gift"*, *"urgent notice"*, or *"password reset"*, which would lose their urgent/phishing context if split into independent tokens.

### Q4: Why combine TF-IDF with handcrafted heuristic features?
**Answer**: Pure NLP models may miss non-linguistic technical signals, such as an IP address substituted in a hyperlink (`http://192.168.1.1/...`) or an unusual proportion of capital letters and exclamation marks. Combining statistical TF-IDF with domain heuristics provides a dual-layer defense that is robust against adversarial keyword stuffing.

### Q5: What evaluation metric is most important here, and why?
**Answer**: While Accuracy provides a baseline, **Recall for the Phishing class** and **Macro F1-Score** are the most critical. In cybersecurity, a False Negative (classifying a Phishing message as Legitimate) is far more dangerous than a False Positive (flagging a legitimate email as suspicious).

### Q6: How does the system handle class imbalance?
**Answer**: Stratified sampling was applied during train-test splitting and 5-fold cross-validation to maintain balanced class proportions across all training and evaluation folds.

### Q7: How does Multinomial Naive Bayes handle zero-frequency words in testing?
**Answer**: It uses Laplace (additive) smoothing (controlled by parameter $\alpha=0.1$). This assigns a small non-zero probability to unseen tokens, preventing the entire probability product from becoming zero.

### Q8: What are potential future enhancements for this project?
**Answer**:
1. Incorporating fine-tuned Transformer models (such as BERT or RoBERTa) for deep contextual semantic understanding.
2. Integrating domain WHOIS / DNS lookup verification to inspect link domains in real-time.
3. Adding a browser extension or email client plugin (e.g., for Outlook or Gmail) for client-side scanning.

---

## 7. Conclusion
The developed system demonstrates that pairing NLP text preprocessing and TF-IDF representations with cybersecurity-aware heuristic engineering yields a highly accurate, lightweight, and explainable message classifier. The accompanying Flask web dashboard delivers instant inference, transparent threat explanations, and an intuitive user interface suitable for educational, research, and practical deployment demonstrations.
