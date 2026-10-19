"""Train every model and save the best one per task.

Run from the project root:
    python -m src.train            # train everything
    python -m src.train heart      # train a single task (symptoms, heart, diabetes, breast)
"""
import json
import sys
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier

from src.data import DATA_DIR, MODEL_DIR, REPORT_DIR, SYMPTOM_TARGET, humanize_symptom, load_symptom_datasets
from src.tabular import TABULAR_TASKS, breast_help, friendly_breast_label

warnings.filterwarnings("ignore")
SEED = 42


def make_models(pos_weight=1.0, multiclass=False):
    xgb_kwargs = dict(n_estimators=250, max_depth=5, learning_rate=0.08, subsample=0.9,
                      colsample_bytree=0.9, tree_method="hist", random_state=SEED, n_jobs=-1)
    if multiclass:
        xgb_kwargs.update(objective="multi:softprob", eval_metric="mlogloss")
    else:
        xgb_kwargs.update(scale_pos_weight=pos_weight, eval_metric="logloss")
    return {
        "SVM": Pipeline([("scaler", StandardScaler()),
                         ("clf", SVC(kernel="rbf", class_weight="balanced",
                                     probability=True, random_state=SEED))]),
        "Logistic Regression": Pipeline([("scaler", StandardScaler()),
                                         ("clf", LogisticRegression(max_iter=5000,
                                                                    class_weight="balanced",
                                                                    random_state=SEED))]),
        "Random Forest": RandomForestClassifier(n_estimators=300, class_weight="balanced_subsample",
                                                random_state=SEED, n_jobs=-1),
        "XGBoost": XGBClassifier(**xgb_kwargs),
    }


# ---------------------------------------------------------------- symptom task
def train_symptoms():
    print("\n=== Symptom checker (multi-class) ===")
    train_df, test_df, features = load_symptom_datasets()
    encoder = LabelEncoder()
    y_train = encoder.fit_transform(train_df[SYMPTOM_TARGET])
    y_test = encoder.transform(test_df[SYMPTOM_TARGET])
    X_train, X_test = train_df[features], test_df[features]

    rows, fitted = [], {}
    for name, model in make_models(multiclass=True).items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        rows.append({
            "Model": name,
            "Accuracy": accuracy_score(y_test, pred),
            "Macro Precision": precision_score(y_test, pred, average="macro", zero_division=0),
            "Macro Recall": recall_score(y_test, pred, average="macro", zero_division=0),
            "Macro F1-score": f1_score(y_test, pred, average="macro", zero_division=0),
        })
        fitted[name] = model
        print(f"  {name:<20} accuracy={rows[-1]['Accuracy']:.3f}  macro F1={rows[-1]['Macro F1-score']:.3f}")

    results = pd.DataFrame(rows).sort_values("Macro F1-score", ascending=False).reset_index(drop=True)
    best_name = results.iloc[0]["Model"]
    joblib.dump(fitted[best_name], MODEL_DIR / "symptoms_model.joblib")
    meta = {
        "task": "symptoms",
        "best_model": best_name,
        "best_macro_f1": round(float(results.iloc[0]["Macro F1-score"]), 4),
        "best_accuracy": round(float(results.iloc[0]["Accuracy"]), 4),
        "features": features,
        "symptom_labels": {f: humanize_symptom(f) for f in features},
        "classes": encoder.classes_.tolist(),
        "metrics": results.round(4).to_dict(orient="records"),
        "n_train": int(len(train_df)), "n_test": int(len(test_df)),
        "source": "Symptom-based disease dataset (Training.csv / Testing.csv)",
        "educational_use_only": True,
    }
    _save_meta("symptoms", meta)
    results.to_csv(REPORT_DIR / "symptoms_model_comparison.csv", index=False)
    return meta


# ---------------------------------------------------------- tabular tasks
def _load_tabular(key):
    cfg = TABULAR_TASKS[key]
    df = pd.read_csv(DATA_DIR / cfg["file"])
    y = df[cfg["target"]].astype(int)
    X = df.drop(columns=[cfg["target"]]).astype(float)
    for col in cfg.get("zero_is_missing", []):
        X[col] = X[col].replace(0, np.nan)
    return X, y


def _schema_for(key, X, features):
    cfg = TABULAR_TASKS[key]
    fields = []
    for name in features:
        col = X[name]
        if key == "breast":
            fields.append({
                "name": name, "label": friendly_breast_label(name), "help": breast_help(name),
                "unit": "", "type": "number",
                "min": float(np.floor(col.min() * 10) / 10), "max": float(np.ceil(col.max() * 10) / 10),
                "step": 0.001, "default": round(float(col.median()), 4),
            })
            continue
        spec = dict(cfg["fields"][name])
        spec["name"] = name
        spec.setdefault("help", "")
        spec.setdefault("unit", "")
        spec["type"] = "select" if "options" in spec else "number"
        fields.append(spec)
    return fields


def train_tabular(key):
    cfg = TABULAR_TASKS[key]
    print(f"\n=== {cfg['title']} ===")
    X, y = _load_tabular(key)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)

    medians = X_tr.median()
    X_tr = X_tr.fillna(medians)
    X_te = X_te.fillna(medians)

    features = list(X.columns)
    if cfg.get("select_top_k"):
        # Choose the most informative measurements using training data only.
        rf = RandomForestClassifier(n_estimators=300, random_state=SEED, n_jobs=-1).fit(X_tr, y_tr)
        ranked = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
        chosen = set(ranked.head(cfg["select_top_k"]).index)
        features = [f for f in features if f in chosen]
        print("  Selected features:", ", ".join(features))
    X_tr, X_te = X_tr[features], X_te[features]

    pos_weight = float((y_tr == 0).sum() / max((y_tr == 1).sum(), 1))
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    rows, fitted = [], {}
    for name, model in make_models(pos_weight=pos_weight).items():
        cv_auc = cross_val_score(clone(model), X_tr, y_tr, cv=cv, scoring="roc_auc").mean()
        model.fit(X_tr, y_tr)
        proba = model.predict_proba(X_te)[:, 1]
        pred = (proba >= 0.5).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_te, pred, labels=[0, 1]).ravel()
        rows.append({
            "Model": name,
            "CV ROC-AUC (train)": round(float(cv_auc), 4),
            "Accuracy": round(accuracy_score(y_te, pred), 4),
            "Sensitivity (recall)": round(recall_score(y_te, pred, zero_division=0), 4),
            "Specificity": round(tn / (tn + fp) if (tn + fp) else 0.0, 4),
            "Precision": round(precision_score(y_te, pred, zero_division=0), 4),
            "F1-score": round(f1_score(y_te, pred, zero_division=0), 4),
            "Test ROC-AUC": round(roc_auc_score(y_te, proba), 4),
            "TP": int(tp), "TN": int(tn), "FP": int(fp), "FN": int(fn),
        })
        fitted[name] = model
        print(f"  {name:<20} CV AUC={cv_auc:.3f}  test AUC={rows[-1]['Test ROC-AUC']:.3f}  "
              f"recall={rows[-1]['Sensitivity (recall)']:.3f}")

    results = pd.DataFrame(rows).sort_values("CV ROC-AUC (train)", ascending=False).reset_index(drop=True)
    best_name = results.iloc[0]["Model"]
    best_row = results.iloc[0]
    joblib.dump(fitted[best_name], MODEL_DIR / f"{key}_model.joblib")

    full_X = X[features]
    meta = {
        "task": key,
        "title": cfg["title"],
        "short": cfg["short"],
        "description": cfg["description"],
        "positive_label": cfg["positive_label"],
        "info_key": cfg["info_key"],
        "source": cfg["source"],
        "best_model": best_name,
        "best_accuracy": float(best_row["Accuracy"]),
        "best_test_auc": float(best_row["Test ROC-AUC"]),
        "best_sensitivity": float(best_row["Sensitivity (recall)"]),
        "features": _schema_for(key, full_X, features),
        "feature_names": features,
        "medians": {k: float(v) for k, v in medians[features].items()},
        "metrics": results.to_dict(orient="records"),
        "n_samples": int(len(X)), "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
        "positive_rate": round(float(y.mean()), 4),
        "educational_use_only": True,
    }
    _save_meta(key, meta)
    results.to_csv(REPORT_DIR / f"{key}_model_comparison.csv", index=False)
    print(f"  Best model: {best_name}")
    return meta


# ------------------------------------------------------------------ helpers
def _save_meta(key, meta):
    MODEL_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    with open(MODEL_DIR / f"{key}_meta.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, default=float)


def train_key(key):
    if key == "symptoms":
        return train_symptoms()
    return train_tabular(key)


def run(keys=None):
    keys = keys or ["symptoms", "heart", "diabetes", "breast"]
    for key in keys:
        train_key(key)
    print("\nDone. Models saved to", MODEL_DIR)


if __name__ == "__main__":
    run(sys.argv[1:] or None)
