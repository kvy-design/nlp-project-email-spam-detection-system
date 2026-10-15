import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MaxAbsScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

# Add src to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocess import CleanTextTransformer, HeuristicFeatureExtractor

def load_data(filepath="data/emails.csv"):
    df = pd.read_csv(filepath)
    X = df["text"].values
    y = df["label"].values
    return X, y

def build_feature_union():
    """Combines TF-IDF N-grams with cybersecurity heuristic features."""
    tfidf_pipe = Pipeline([
        ("cleaner", CleanTextTransformer()),
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=3000,
            sublinear_tf=True
        ))
    ])
    
    heuristic_pipe = Pipeline([
        ("extractor", HeuristicFeatureExtractor()),
        ("scaler", MaxAbsScaler()) # Preserves sparsity and non-negativity for Naive Bayes
    ])
    
    union = FeatureUnion([
        ("tfidf_branch", tfidf_pipe),
        ("heuristic_branch", heuristic_pipe)
    ])
    
    return union

def evaluate_models(X_train, X_test, y_train, y_test):
    feature_union = build_feature_union()
    
    candidates = {
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
        "Logistic Regression": LogisticRegression(max_iter=1000, C=2.0, random_state=42),
        "Support Vector Machine (Linear)": CalibratedClassifierCV(LinearSVC(dual=False, random_state=42)),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    }
    
    results = {}
    best_name = None
    best_f1 = -1.0
    best_pipeline = None
    
    classes = sorted(list(set(y_train)))
    
    for name, clf in candidates.items():
        pipe = Pipeline([
            ("features", build_feature_union()),
            ("classifier", clf)
        ])
        
        # 5-Fold Stratified Cross Validation
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(pipe, X_train, y_train, cv=skf, scoring="f1_macro")
        
        # Train on full train set
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        macro_f1 = f1_score(y_test, y_pred, average="macro")
        weighted_f1 = f1_score(y_test, y_pred, average="weighted")
        
        rep = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_test, y_pred, labels=classes).tolist()
        
        results[name] = {
            "cv_macro_f1_mean": float(np.round(cv_scores.mean(), 4)),
            "cv_macro_f1_std": float(np.round(cv_scores.std(), 4)),
            "test_accuracy": float(np.round(acc, 4)),
            "macro_f1": float(np.round(macro_f1, 4)),
            "weighted_f1": float(np.round(weighted_f1, 4)),
            "per_class": {
                c: {
                    "precision": float(np.round(rep[c]["precision"], 4)),
                    "recall": float(np.round(rep[c]["recall"], 4)),
                    "f1_score": float(np.round(rep[c]["f1-score"], 4)),
                    "support": int(rep[c]["support"])
                } for c in classes if c in rep
            },
            "confusion_matrix": cm,
            "classes": classes
        }
        
        print(f"[{name}] Test Acc: {acc:.4f} | Macro F1: {macro_f1:.4f} | 5-Fold CV F1: {cv_scores.mean():.4f}")
        
        if macro_f1 > best_f1:
            best_f1 = macro_f1
            best_name = name
            best_pipeline = pipe
            
    print(f"\n>>> Selected Best Model: {best_name} with Macro F1: {best_f1:.4f}")
    return best_name, best_pipeline, results

def main():
    print("Loading email dataset...")
    X, y = load_data()
    print(f"Loaded {len(X)} records across classes: {np.unique(y)}")
    
    # 80/20 Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")
    
    print("\nTraining and evaluating candidate algorithms...")
    best_name, best_pipeline, results = evaluate_models(X_train, X_test, y_train, y_test)
    
    os.makedirs("models", exist_ok=True)
    model_save_path = os.path.join("models", "model.pkl")
    joblib.dump({
        "pipeline": best_pipeline,
        "best_model_name": best_name,
        "classes": sorted(list(set(y_train)))
    }, model_save_path)
    print(f"\nModel pipeline saved to: {model_save_path}")
    
    metrics_path = os.path.join("models", "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({
            "best_model": best_name,
            "models": results,
            "train_size": len(X_train),
            "test_size": len(X_test)
        }, f, indent=2)
    print(f"Evaluation metrics saved to: {metrics_path}")

if __name__ == "__main__":
    main()
