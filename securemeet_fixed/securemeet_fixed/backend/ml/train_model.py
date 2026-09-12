"""
SecureMeet — ML Moderation Model
Trained on Jigsaw Toxic Comment Classification Dataset (Kaggle)
Uses a balanced sample for memory-efficient Docker builds.
"""

import os, pickle, re, csv
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_CSV   = os.path.join(BASE_DIR, "train.csv")
MODEL_PATH = os.path.join(BASE_DIR, "moderation_model.pkl")
VECTR_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
META_PATH  = os.path.join(BASE_DIR, "model_meta.pkl")

def clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s!?.,]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_action(row: dict) -> tuple:
    flags = {k: int(row[k]) for k in ["toxic","severe_toxic","obscene","threat","insult","identity_hate"]}
    active = [k for k, v in flags.items() if v == 1]
    if not active:
        return False, "allow", []
    if flags["threat"] or flags["identity_hate"]: action = "ban"
    elif flags["severe_toxic"]:                   action = "mute"
    elif flags["obscene"] or flags["insult"]:     action = "filter"
    else:                                         action = "warning"
    return True, action, active

print("[Train] Loading Jigsaw dataset...")
toxic_texts, clean_texts = [], []

with open(DATA_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        is_toxic, action, _ = get_action(row)
        t = clean(row["comment_text"])
        if is_toxic:
            toxic_texts.append(t)
        else:
            clean_texts.append(t)

print(f"[Train] Toxic: {len(toxic_texts)} | Clean: {len(clean_texts)}")

# Balance: all toxic + 3x toxic count of clean samples
np.random.seed(42)
n_clean = min(len(toxic_texts) * 3, len(clean_texts))
clean_sample = np.random.choice(clean_texts, size=n_clean, replace=False).tolist()

texts  = toxic_texts + clean_sample
labels = [1]*len(toxic_texts) + [0]*len(clean_sample)

# Shuffle
idx = list(range(len(texts)))
np.random.shuffle(idx)
texts  = [texts[i]  for i in idx]
labels = [labels[i] for i in idx]

print(f"[Train] Balanced dataset: {len(texts)} samples")

print("[Train] Fitting TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(
    max_features=30000,
    ngram_range=(1, 2),
    sublinear_tf=True,
    min_df=2,
    strip_accents="unicode",
)
X = vectorizer.fit_transform(texts)
y = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("[Train] Training Logistic Regression...")
model = LogisticRegression(C=5.0, max_iter=500, solver="lbfgs", class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc    = (y_pred == y_test).mean()
print(classification_report(y_test, y_pred, target_names=["clean","toxic"]))
print(f"[Train] Accuracy: {acc*100:.2f}%")

with open(MODEL_PATH, "wb") as f: pickle.dump(model, f)
with open(VECTR_PATH, "wb") as f: pickle.dump(vectorizer, f)
with open(META_PATH,  "wb") as f:
    pickle.dump({
        "accuracy":    round(acc, 4),
        "n_train":     X_train.shape[0],
        "n_features":  X_train.shape[1],
        "data_source": "Jigsaw Toxic Comment Classification (Kaggle)",
    }, f)

print("[Train] Model saved successfully.")
