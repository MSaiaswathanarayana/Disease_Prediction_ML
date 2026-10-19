"""Data loading and cleaning for every prediction task."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"
SYMPTOM_TARGET = "prognosis"

DISEASE_FIXES = {
    "Peptic ulcer diseae": "Peptic ulcer disease",
    "Dimorphic hemmorhoids(piles)": "Hemorrhoids (piles)",
    "(vertigo) Paroymsal Positional Vertigo": "Benign positional vertigo",
    "Osteoarthristis": "Osteoarthritis",
}


def clean_disease_name(name: str) -> str:
    name = " ".join(str(name).split())
    return DISEASE_FIXES.get(name, name)


def clean_symptom_key(column: str) -> str:
    return " ".join(column.replace("_ ", "_").split())


def humanize_symptom(key: str) -> str:
    text = " ".join(key.replace("_", " ").split())
    return text[:1].upper() + text[1:]


def load_symptom_datasets():
    """Return cleaned training and testing frames for the symptom dataset, plus feature names."""
    train = pd.read_csv(DATA_DIR / "Training.csv")
    test = pd.read_csv(DATA_DIR / "Testing.csv")

    def tidy(df):
        df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")].copy()
        df.columns = [SYMPTOM_TARGET if c == SYMPTOM_TARGET else clean_symptom_key(c)
                      for c in df.columns]
        df[SYMPTOM_TARGET] = df[SYMPTOM_TARGET].map(clean_disease_name)
        return df

    train, test = tidy(train), tidy(test)
    features = [c for c in train.columns if c != SYMPTOM_TARGET]
    for df in (train, test):
        for col in features:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    missing = set(features) - set(test.columns)
    if missing:
        raise ValueError(f"Testing.csv is missing features: {sorted(missing)}")
    return train, test, features
