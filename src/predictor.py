"""Load trained models and produce predictions for every task."""
import json
import threading

import joblib
import numpy as np
import pandas as pd

from src.data import MODEL_DIR

MIN_SYMPTOMS = 3
TOP_K = 3
from src.tabular import TABULAR_TASKS as _TABULAR

ALL_TASKS = ["symptoms"] + list(_TABULAR)
REQUIRED = {"symptoms": {"best_model", "features", "symptom_labels", "classes"}}
REQUIRED_TABULAR = {"best_model", "features", "positive_label", "metrics"}

_lock = threading.RLock()
_cache = {}


def _artifacts_ready(key):
    meta_path = MODEL_DIR / f"{key}_meta.json"
    model_path = MODEL_DIR / (f"{key}_model.joblib" if key != "symptoms" else "symptoms_model.joblib")
    if not (meta_path.exists() and model_path.exists()):
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    required = REQUIRED.get(key, REQUIRED_TABULAR)
    return required.issubset(meta)


def load_meta(key):
    """Return the metadata for a task, training the models first if they are missing."""
    with _lock:
        if not _artifacts_ready(key):
            print(f"Model for '{key}' is missing or incomplete. Training now...")
            from src.train import train_key
            train_key(key)
    return json.loads((MODEL_DIR / f"{key}_meta.json").read_text(encoding="utf-8"))


class SymptomPredictor:
    def __init__(self):
        self.meta = load_meta("symptoms")
        self.model = joblib.load(MODEL_DIR / "symptoms_model.joblib")
        self.features = self.meta["features"]
        self.index = {f: i for i, f in enumerate(self.features)}
        self.classes = self.meta["classes"]

    @property
    def symptoms(self):
        items = [{"key": k, "label": v} for k, v in self.meta["symptom_labels"].items()]
        return sorted(items, key=lambda s: s["label"].lower())

    def predict(self, selected_keys, top_k=TOP_K):
        vector = np.zeros((1, len(self.features)))
        used = []
        for key in dict.fromkeys(selected_keys):
            if key in self.index:
                vector[0, self.index[key]] = 1
                used.append(key)
        frame = pd.DataFrame(vector, columns=self.features)
        proba = self.model.predict_proba(frame)[0]
        order = np.argsort(proba)[::-1][:top_k]
        results = [{"disease": self.classes[int(self.model.classes_[i])],
                    "probability": round(float(proba[i]) * 100, 1)} for i in order]
        return results, used


class TabularPredictor:
    def __init__(self, key):
        self.key = key
        self.meta = load_meta(key)
        self.model = joblib.load(MODEL_DIR / f"{key}_model.joblib")
        self.features = self.meta["feature_names"]
        self.schema = {f["name"]: f for f in self.meta["features"]}

    def validate(self, values):
        """Return (clean_values, errors). Checks every required field is present and in range."""
        clean, errors = {}, []
        for name in self.features:
            field = self.schema[name]
            raw = values.get(name)
            if raw is None or raw == "":
                errors.append(f"{field['label']} is required.")
                continue
            try:
                number = float(raw)
            except (TypeError, ValueError):
                errors.append(f"{field['label']} must be a number.")
                continue
            if field["type"] == "select":
                allowed = [float(o[0]) for o in field["options"]]
                if number not in allowed:
                    errors.append(f"{field['label']} has an invalid choice.")
                    continue
            elif not (field["min"] <= number <= field["max"]):
                errors.append(f"{field['label']} should be between {field['min']} and {field['max']}.")
                continue
            clean[name] = number
        return clean, errors

    def predict(self, values):
        clean, errors = self.validate(values)
        if errors:
            return None, errors
        frame = pd.DataFrame([[clean[f] for f in self.features]], columns=self.features)
        p = float(self.model.predict_proba(frame)[0][1])
        if p < 0.3:
            level, text = "Lower", "The model finds a lower likelihood of"
        elif p < 0.6:
            level, text = "Moderate", "The model finds a moderate likelihood of"
        else:
            level, text = "Higher", "The model finds a higher likelihood of"
        return {
            "probability": round(p * 100, 1),
            "risk_level": level,
            "risk_text": f"{text} {self.meta['positive_label']} based on these results.",
        }, []


_predictors = {}


def get_predictor(key):
    if key not in _predictors:
        with _lock:
            if key not in _predictors:
                _predictors[key] = SymptomPredictor() if key == "symptoms" else TabularPredictor(key)
    return _predictors[key]
