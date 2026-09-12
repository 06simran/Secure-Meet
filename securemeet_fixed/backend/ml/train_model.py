"""
SecureMeet — ML Training Script
================================
Train TF-IDF + Logistic Regression toxicity classifier.

Usage:
    python ml/train_model.py                  # uses built-in sample data
    python ml/train_model.py --data path.csv  # uses Jigsaw CSV
"""

import argparse, re
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix,
)

ML_DIR          = Path(__file__).parent
MODEL_OUT       = ML_DIR / "toxicity_model.pkl"
VECTORIZER_OUT  = ML_DIR / "vectorizer.pkl"

SAMPLE_DATA = {
    "text": [
        "You are so stupid, I hate you",
        "Die you worthless idiot",
        "I will kill you if you say that again",
        "Shut up you dumb fool, nobody wants you here",
        "You deserve to suffer and feel pain",
        "Stop spamming buy now free money click here",
        "I will hurt you so badly you regret this",
        "You are pathetic and disgusting",
        "Great meeting today everyone!",
        "Can we reschedule to tomorrow?",
        "Please share the presentation slides.",
        "Looking forward to working with you all.",
        "Let us wrap up in 5 minutes.",
        "Does anyone have questions about the project?",
        "Good job on the deliverable this sprint!",
        "I agree with your points on the architecture.",
        "Thank you for the detailed update.",
        "See you next week at the standup.",
        "The deployment went smoothly today.",
        "Excellent work on the documentation!",
    ],
    "label": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}


def preprocess(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_data(csv_path):
    if csv_path and Path(csv_path).exists():
        print(f"[train] Loading dataset from {csv_path}")
        df = pd.read_csv(csv_path)
        label_cols = [c for c in ["toxic","severe_toxic","obscene","threat","insult","identity_hate"] if c in df.columns]
        if label_cols:
            df["label"] = (df[label_cols].sum(axis=1) > 0).astype(int)
        elif "toxic" in df.columns:
            df["label"] = df["toxic"].astype(int)
        else:
            raise ValueError("No label column found in CSV.")
        return df[["comment_text", "label"]].rename(columns={"comment_text":"text"}).dropna()
    print("[train] Using built-in sample dataset")
    return pd.DataFrame(SAMPLE_DATA)


def train(csv_path=None):
    df = load_data(csv_path)
    df["text"] = df["text"].apply(preprocess)
    print(f"[train] Dataset: {len(df)} rows | toxic={df['label'].sum()} | clean={(df['label']==0).sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    vectorizer = TfidfVectorizer(max_features=50_000, ngram_range=(1,2), sublinear_tf=True, min_df=1)
    X_train_v  = vectorizer.fit_transform(X_train)
    X_test_v   = vectorizer.transform(X_test)

    model = LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced", solver="lbfgs")
    model.fit(X_train_v, y_train)

    y_pred = model.predict(X_test_v)
    print("\n" + "="*55)
    print("  SecureMeet Toxicity Model — Evaluation")
    print("="*55)
    print(f"  Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision : {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  Recall    : {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  F1 Score  : {f1_score(y_test, y_pred, zero_division=0):.4f}")
    print(classification_report(y_test, y_pred, target_names=["Clean","Toxic"], zero_division=0))
    print("  Confusion Matrix:", confusion_matrix(y_test, y_pred))
    print("="*55 + "\n")

    joblib.dump(model,      MODEL_OUT)
    joblib.dump(vectorizer, VECTORIZER_OUT)
    print(f"[train] Saved model      → {MODEL_OUT}")
    print(f"[train] Saved vectorizer → {VECTORIZER_OUT}")
    print("[train] Done ✓")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=None)
    args = parser.parse_args()
    train(args.data)
