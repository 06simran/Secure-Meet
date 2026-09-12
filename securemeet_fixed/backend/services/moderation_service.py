import os, pickle, re
import numpy as np

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ML_DIR     = os.path.join(BASE_DIR, "..", "ml")
MODEL_PATH = os.path.join(ML_DIR, "moderation_model.pkl")
VECTR_PATH = os.path.join(ML_DIR, "tfidf_vectorizer.pkl")
META_PATH  = os.path.join(ML_DIR, "model_meta.pkl")

_model = None
_vectorizer = None
_meta = None

def _load():
    global _model, _vectorizer, _meta
    if _model is not None:
        return
    try:
        with open(MODEL_PATH, "rb") as f: _model      = pickle.load(f)
        with open(VECTR_PATH, "rb") as f: _vectorizer = pickle.load(f)
        with open(META_PATH,  "rb") as f: _meta       = pickle.load(f)
        print(f"[ModerationService] Jigsaw model loaded ✓")
    except FileNotFoundError:
        print("[ModerationService] Model not found — using rule-based fallback")

def _clean(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s!?.,]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

_TOXIC_WORDS = ["idiot","stupid","kill","hate","die","loser","racist","nazi","threat","abuse"]

def _rule_based(text):
    hits = [w for w in _TOXIC_WORDS if w in text.lower()]
    if not hits:
        return {"toxic": False, "confidence": 0.05, "labels": [], "action": "allow", "model": "rule-based"}
    conf = min(0.95, 0.5 + len(hits) * 0.15)
    return {"toxic": True, "confidence": conf, "labels": hits, "action": "warning", "model": "rule-based"}

def _action(confidence):
    if confidence >= 0.90: return "ban"
    if confidence >= 0.75: return "mute"
    if confidence >= 0.55: return "filter"
    return "warning"

def moderate(text):
    _load()
    if _model is None:
        return _rule_based(text)
    X = _vectorizer.transform([_clean(text)])
    prob = float(_model.predict_proba(X)[0][1])
    toxic = prob >= 0.5
    return {
        "toxic":      toxic,
        "confidence": round(prob, 4),
        "labels":     ["toxic"] if toxic else [],
        "action":     _action(prob) if toxic else "allow",
        "model":      "jigsaw-logreg",
    }

def get_model_info():
    _load()
    if _meta is None:
        return {"model": "rule-based"}
    return _meta

class ModerationService:
    def analyze(self, text):
        return moderate(text)
    def get_info(self):
        return get_model_info()


class ModerationService:
    def analyze(self, text):
        return moderate(text)
    def get_info(self):
        return get_model_info()
